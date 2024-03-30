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


- __customer_idx 컬럼__



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
