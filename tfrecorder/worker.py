import itertools
import logging
import multiprocessing
import os
from typing import Awaitable

import tqdm

from .config import Config, ExecutionMode
from .convert import Converter
from .fileio import get_filenames, save_tfrecord_file
from .upload import Uploader
from .utils import batch


class Worker:
    def __init__(self, config: Config, log: bool = True):
        self.config: Config = config
        self.log: bool = True

    async def run(self) -> Awaitable[None]:
        if self.config.exec_mode == ExecutionMode.CONVERT_AND_UPLOAD:
            pass
        elif self.config.exec_mode == ExecutionMode.CONVERT:
            await self.convert()
        else:
            await self.upload()

    async def convert_and_upload(self) -> Awaitable[None]:
        # TODO: Convert and upload simultaneously; with asyncio Queue
        await self.convert()
        await self.upload()

    async def convert(self) -> Awaitable[None]:
        self._log(f"Obtaining filenames from from_path...")
        filenames = get_filenames(self.config.from_path)
        self._log(f"{len(filenames)} files were found")
        pool_size = min(self.config.max_pool_size, len(filenames))

        self._log(f"Start to convert with pool size {pool_size}")
        with multiprocessing.Pool(pool_size) as pool:
            converter = Converter(self.config)
            argument_pack = zip(filenames, itertools.repeat(self.config))
            results = list(
                tqdm.tqdm(
                    pool.imap_unordered(converter.convert_one_file, argument_pack, chunksize=self.config.chunk_size),
                    total=len(filenames),
                )
            )
        examples = [example for result in results for example in result[0]]
        self._log(f"All {sum([item[1] for item in results])} records are converted")
        self._log(f"Finished to convert. Saving files...")

        tfrecord_path = os.path.dirname(self.config.to_path)
        os.makedirs(tfrecord_path, exist_ok=True)
        for idx, example_batch in enumerate(batch(examples, self.config.batch_size)):
            filename = tfrecord_path + f"/{self.config.name}.{idx:04d}.tfrecord"
            save_tfrecord_file(example_batch, filename, compression_type=self.config.compression_type)

        self._log(f"Finished to save.")

    async def upload(self) -> Awaitable[None]:
        self._log(f"Obtaining filenames from to_path...")
        filenames = get_filenames(self.config.to_path)
        self._log(f"{len(filenames)} files were found")
        pool_size = min(self.config.max_pool_size, len(filenames))

        self._log(f"Start to upload with pool size {pool_size}")
        with multiprocessing.Pool(pool_size) as pool:
            uploader = Uploader(self.config)
            results = list(
                tqdm.tqdm(
                    pool.imap_unordered(
                        lambda filename: uploader.upload_file(filename), filenames, chunksize=self.config.chunk_size
                    ),
                    total=len(filenames),
                )
            )

        self._log(f"{sum(results)} / {len(filenames)} files were uploaded")

    def _log(self, *args, **kwargs):
        if self.log:
            logging.info(args, kwargs)
