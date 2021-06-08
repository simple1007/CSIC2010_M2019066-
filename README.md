# CSIC2010_M2019066-
2021년 국민대학교 정보보호특론 CSIC2010 프로젝트 데이터셋

- 원시 데이터셋
anomal_test.txt
anomal_train.txt
norm_test.txt
norm_train.txt

- 데이터셋(train.csv, test.csv)를 만들기 위한 temp파일
anomal_test_gen.txt
anomal_train_gen.txt
norm_test_gen.txt
norm_train_gen.txt

- 훈련/test 데이터셋
train.csv
test.csv

- data_.py
데이터셋(train.csv, test.csv) 생성 코드
유니그램 바이그램 사전생성
(실행)
python data_.py
vocab_post.pkl(바이그램 사전 파일) vocab_char.pkl(유니그램 사전 파일)
 
content_type.pkl accept.pkl vocab_get.pkl ( temp 파일 현재 사용 안함 )

- train.py
유니그램 훈련 코드

- train2.py
바이그램 훈련 코드

- security
유니그램 모델 파일

- security_bigram
바이그램 모델 파일

- test_uni.py
유니그램 모델 평가 코드

- test_bi.py
바이그램 모델 평가 코드

- 새노트북.ipynb
모델 평가 노트북 파일
