# TFRecorder

> NLP Dataset을 TFRecord로 바꾸고, GPU/TPU 학습을 위해 Cloud Storage에 올려주는 CLI 도구

## 핵심 기능

- [x] CSV, TSV 파일들을 Metadata를 바탕으로 TFRecord로 변환
- [x] TensorFlow에서 TPU로 학습할 때 유용하도록 변환한 파일들을 Google Cloud Storage로 업로드
- [ ] `asyncio.Queue`를 사용해서 위 두 개의 과정이 동시에 이루어지도록 함

## Metadata 파일 작성 방법

```json
{
  "name": "<Dataset의 이름으로, TFRecord 파일의 이름과 Google Cloud Storage Bucket의 이름으로 사용됩니다.>",
  "convert": {
    "from_path": "<변환할 Dataset의 경로입니다. Glob 패턴으로 기술합니다.>",
    "file_type": "<파일의 형식입니다. 'csv'나 'tsv'로 사용합니다.>",
    "skip_header": false
  },
  "columns": [
    {
      "name": "<열의 이름입니다.>",
      "feature_type": "<열의 자료형입니다. 'str', 'bool', 'int', 'float'>"
    }
  ]
}
```

## 도구 사용 방법

```text
$ tfr -h
usage: tfr [-h] [-m MODE] [--max-error MAX_ERROR] [-c COMPRESSION_TYPE]
           [--only-convert [ONLY_CONVERT]] [--only-upload [ONLY_UPLOAD]]
           [--batch-size BATCH_SIZE] [-g GOOGLE_APPLICATION_CREDENTIALS]
           [--max-pool-size MAX_POOL_SIZE] [--chunksize CHUNKSIZE]
           METADATA_PATH

Automatically convert CSV or TSV files to TFRecord, and upload them to Google
Cloud Storage.

positional arguments:
  METADATA_PATH         Path of JSON file which have metadata

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Method to parse the file. Use tsv by default.
  --max-error MAX_ERROR
                        Max error records while parsing. Not set (-1) by
                        default.
  -c COMPRESSION_TYPE, --compression-type COMPRESSION_TYPE
                        TFRecord compression type. Use GZIP by default.
  --only-convert [ONLY_CONVERT]
                        Only convert the files, not upload to GCS
  --only-upload [ONLY_UPLOAD]
                        Only upload the files to GCS, not convert (will read
                        TFRECORD_PATH only)
  --batch-size BATCH_SIZE
                        Size of the examples one file should have. Use 1000 by
                        default.
  -g GOOGLE_APPLICATION_CREDENTIALS, --google-application-credentials GOOGLE_APPLICATION_CREDENTIALS
                        Google Application Credential JSON file path. Will use
                        environment variable as a default.
  --max-pool-size MAX_POOL_SIZE
                        Max pool size for multiprocessing. Use all cores by
                        default.
  --chunksize CHUNKSIZE
                        Chunksize for multiprocessing. Use 10 by default.
```

## 테스트

이 도구를 테스트하려면, 프로젝트를 Clone하신 후 다음 내용을 입력하십시오.

```bash
python setup.py develop
```
