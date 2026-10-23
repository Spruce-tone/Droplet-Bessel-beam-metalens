# Droplet Bessel beam metalens (DBBM)

[English](README.md) | 한국어

**직경 200 µm 위상·진폭 설계 → LCP/RCP 전파 → 합친 PSF 표시**를 실행하는 독립형 CPU 데모입니다.
하다마드·MMISM과 동일하게 `demo.ipynb`, `lib/`, `docker/`, `images/`로 구성했습니다.

## 실행

Docker Desktop의 Linux 컨테이너 모드에서 이 폴더를 기준으로 실행합니다.

```bash
docker compose -f docker/compose.yaml up --build
```

로그의 토큰 포함 Jupyter 주소에서 포트 8888을 **8890**으로 바꿔 접속합니다.
`demo.ipynb`를 열고 **Restart Kernel and Run All Cells**를 실행합니다.
CPU 2개·메모리 8 GiB 제한이며 GPU나 입력 데이터가 필요하지 않습니다.
종료: `docker compose -f docker/compose.yaml down`.

Python 3.12 직접 실행:

```bash
python -m pip install -r docker/requirements.txt
python -m jupyter lab demo.ipynb
```

## 계산 흐름

1. 외측 직경 200 µm, 내측 직경 100 µm인 두 링에 같은 구면 렌즈 위상을 적용합니다. 두 링의 방사 방향 폭은 각각 5 µm입니다.
2. RCP의 안쪽 링에만 π를 추가하고, LCP/RCP를 MMISM과 같은 ASM으로 각각 전파합니다.
3. 동일한 입사 편광 비중과 편광 비분해 검출을 가정하여, 정규화 전 강도를 `(I_LCP + I_RCP) / 2`로 합칩니다. 이때 링 사이 간섭항이 상쇄됩니다.
4. 초점 XY·축 방향 XZ PSF와 원시 강도 단면을 표시합니다. 이미지 비교에는 공통 최댓값을 사용합니다.

![위상 및 진폭](images/phases.png)
![초점 PSF](images/result.png)
![축 방향 PSF](images/axial_psf.png)
![원시 강도 프로파일](images/line_profile.png)

파장 633 nm, NA 0.3, 설계 초점 317.980 µm, 격자 800², 간격 0.25 µm이며,
전파 격자는 1600²로 패딩합니다. 축 방향은 z = 150–399.9 µm를 0.3 µm 간격(834개 평면)으로 계산합니다.
기본값은 데모 조건이며 최적화 결과가 아닙니다.

## 검증과 범위

공개 노트북은 파라미터·설계·초점 PSF·축 방향 PSF의 코드 셀 4개로 구성합니다.
수치 검산은 개발 중 별도로 수행하며 데모에서는 제외했습니다.
원본 연구 코드에서 링·렌즈 위상 식만 가져왔으며, GPU RS 전파는 MMISM의 ASM으로 대체했습니다.
메타원자 효율·편광 누설·벡터 전파·제작·이미지 복원은 포함하지 않습니다.
유한 격자 및 FFT 경계 오차가 남을 수 있으며 2배 패딩은 전체 수렴 검증을 의미하지 않습니다.
전체 3D 볼륨 대신 필요한 단면만 저장합니다. 중앙 행의 역 FFT만 계산하고 고정 거리 간격의 전파 위상을 누적하여 같은 이산 ASM을 빠르게 계산합니다. 넓어진 범위는 주요 PSF와 감쇠 꼬리를 보여주며 수학적으로 무한한 PSF 전체를 뜻하지 않습니다.

노트북, 최소 `lib/`, Docker 설정, 생성 이미지, 영문·한국어 README를 함께 배포합니다.
코드 재사용 시 `LICENSE`, `licenses/`, `THIRD_PARTY_NOTICES.md`를 유지하십시오.
주변 데모는 GPL-3.0이며 diffractsim 부분은 원래 MPL 2.0 고지를 보존합니다.

노트북 코드 셀 4개를 DBBM Docker 환경에서 실행해 결과를 저장했습니다.

x·y 간격은 얇은 링의 강도 반치폭 근사값 0.358 λ/NA ≈ 0.755 µm를 기준으로 최소 3개 샘플을 확보합니다. FFT를 위해 격자 수를 32의 배수로 올림하여 800², dx = dy = 0.25 µm(반치폭당 3.022개 샘플)를 사용합니다. 실제 합산 PSF 반치폭은 별도로 검산했습니다. 사용자가 선택한 축 범위 150–399.9 µm를 유지하므로 모든 감쇠 꼬리가 포함되지는 않습니다.
