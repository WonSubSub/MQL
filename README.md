# MQL 데이터 기반 B2B 고객의 영업 전환 여부 예측
## 프로젝트 목표  
* MQL 데이터를 기반으로 영업 전환 성공 확률이 낮은 잠재 고객의 특징 파악
 
    &xrarr; 모델이 예측하기 어려운 잠재 고객의 특징 파악 
---

<details><summary>Dataset</summary>

- __Categorical columns__


| Column Name  | Description | dType  | Null_percentage  |
|:-------------:|:-------------:|:-------------:|:-------------:|
| business_unit |사업부| str| 0% |
| customer_idx |회사 고유 Index| int| 0% |
| customer_type |고객 유형| str| 74% |
| enterprise |회사 규모 | str| 0% |
| customer_job |고객 업종 | str| 32% |
| inquiry_type |문의 유형| str| 2% |
| product_category |제품 대분류| str| 33% |
| product_subcategory |제품 중분류| str| 84% |
| product_modelname |제품 모델명| str| 84% |
| customer_position |고객 직책| str| 0% |
| response_corporate |담당 법인| str| 0% |
| expected_timeline |희망 구매 날짜| str| 52% |
| business_area |사업 도메인|str | 69% |
| business_subarea |사업 세부 도메인|str | 91% |
| lead_owner |영업 담당자|int | 0% |


- __Numerical columns__

  
| Column Name  | Description | dType  | Null_percentage  |
|:-------------:|:-------------:|:-------------:|:-------------:|
|bant_submit |MQL 정보의 BANT 가중치|float| 0% |
|historical_existing_cnt |과거 영업 전환 횟수|int| 77% |
|lead_desc_length |고객 요청사항의 글자 수|int| 0% |


- __Target column__


| Column Name  | Description | dType  | True_percentage  |
|:-------------:|:-------------:|:-------------:|:-------------:|
|is_converted |영업 전환 성공 여부|bool| 8.2% |

</details>

#

<details><summary>EDA</summary>

<br>

- __is_converted 컬럼 (영업 전환 성공 여부)__ : _Target Column_  
>![text](/image/customer_idx1)  
>>--> Target 컬럼의 심한 데이터 불균형  
__&xrarr; 오버샘플링, 임계값 조정 고려__
<br>

- __customer_idx 컬럼 (고객 회사의 고유 idx)__  
>![text](/image/customer_idx1)  
customer_idx가 20596인 값들은 모두 영업 전환에 성공, 모두 customer_type 값이 결측치  
>>--> customer_type이 결측치, 영업 전환 성공한한 회사 중 회사 idx를 분실(?)한 customer_idx가 모두 25096으로 추정  
__&xrarr; 모델 학습시 25096에 대한 오버피팅을 막기 위해 별도의 전처리 적용__

<br>

- __customer_type 컬럼 (고객 유형)__  
>customer_type의 결측 유무에 따른 영업 성공 비율  
결측 O ------------------------결측 X  
![text](/image/customer_type1)
![text](/image/customer_type2)  
>>--> customer_type 값이 존재할 때 영업 전환 성공 비율이 약 두배 높음, 결측 비율이 77%로 결측치가 상당히 많음   
__&xrarr; customer_type 값이 결측치가 아닌 데이터셋을 따로 구성 후 새로운 모델 구성__

<br>

- __lead_owner 컬럼 (영업 담당자)__  
>영업에 항상 성공하는 영업 담당자가 있는 반면 영업 횟수가 많음에도 항상 실패하는 영업 담당자가 존재   
--> 영업 담당자 개개인의 역량 차이가 심함  
![text](/image/lead_owner1)  
>>분석의 주 목적은 잠재 고객을 찾는 것이기 때문에 영업 담장자의 개인 역량이 관여해서는 안됨  
__&xrarr; lead_owner 컬럼은 학습에 활용 X__ _(실제로 학습에 활용 했을시 F1_score 기준으로 약 0.2 상승)_

<br>

- __lead_desc_length 컬럼 (고객이 작성한 요청사항의 글자 수)__  
>value_counts 값이 유독 높은 데이터 값 = 3, 14  
--> lead_desc_length 값이 1 ~ 20에 있는 데이터들을 시각화   
![text](/image/lead_desc_length1)
![text](/image/lead_desc_length2)  
>>--> lead_desc_length 값이 3인 데이터들은 영업 전환 성공 비율이 주위 데이터에 비해 높은 편  
--> lead_desc_length 값이 14인 데이터들은 영업 전환 성공 비율이 매우 낮음  
 __&xrarr; lead_desc_length 컬럼의 결측치가 전혀 없는 것을 고려하여 값이 정확한 특징이 파악되지 않는 3, 14 값을 결측치 취급__ _(median 값으로 대체)_  
>  
>lead_desc_length의 분포 확인  
![text](/image/lead_desc_length2)  
>>--> 데이터가 왼쪽으로 쏠림  
__&xrarr; 분포 변환 적용 고려__  
>  
>value_counts 값이 20개 이상인 데이터들의 lead_desc_length(x) 별 영업 성공 비율(y) 분포 확인  
![text](/image/lead_desc_length2)  
>> --> lead_desc_length와 영업 전환 성공률은 어느정도 비례 관계가 있는 것으로 판단 가능



</details>

#

<details><summary>Validation Set</summary>

* .

</details>

#

<details><summary>Preprocessing</summary>

* .

</details>

#

<details><summary>Modeling</summary>

* .

</details>

#

<details><summary>Ensemble</summary>

* .

</details>

#

<details><summary>Result</summary>

* .

</details>

#
