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
>![cutomer_idx1](/img/customer_idx1.png)  
>>--> Target 컬럼의 심한 데이터 불균형  
__&xrarr; 오버샘플링, 임계값 조정 고려__


#
<br>

- __customer_idx 컬럼 (고객 회사의 고유 idx)__  
>![customer_idx2](/img/customer_idx1.png)  
customer_idx가 20596인 값들은 모두 영업 전환에 성공, 모두 customer_type 값이 결측치  
>>--> customer_type이 결측치, 영업 전환 성공한한 회사 중 회사 idx를 분실(?)한 customer_idx가 모두 25096으로 추정  
__&xrarr; 모델 학습시 25096에 대한 오버피팅을 막기 위해 별도의 전처리 적용__


#
<br>

- __customer_type 컬럼 (고객 유형)__  
>customer_type의 결측 유무에 따른 영업 성공 비율  
결측 O &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;결측 X  
![customer_type1](/img/customer_type1.png)
![customer_type2](/img/customer_type2.png)  
>>--> customer_type 값이 존재할 때 영업 전환 성공 비율이 약 두배 높음, 결측 비율이 77%로 결측치가 상당히 많음   
__&xrarr; customer_type 값이 결측치가 아닌 데이터셋을 따로 구성 후 새로운 모델 구성__


#
<br>

- __lead_owner 컬럼 (영업 담당자)__  
>영업에 항상 성공하는 영업 담당자가 있는 반면 영업 횟수가 많음에도 항상 실패하는 영업 담당자가 존재   
--> 영업 담당자 개개인의 역량 차이가 심함  
![lead_owner1](/img/lead_owner1.png)  
>>분석의 주 목적은 잠재 고객을 찾는 것이기 때문에 영업 담장자의 개인 역량이 관여해서는 안됨  
__&xrarr; lead_owner 컬럼은 학습에 활용 X__ _(실제로 학습에 활용 했을시 F1_score 기준으로 약 0.2 상승)_


# 
<br>

- __lead_desc_length 컬럼 (고객이 작성한 요청사항의 글자 수)__  
>value_counts 값이 유독 높은 데이터 값 = 3, 14  
--> lead_desc_length 값이 1 ~ 20에 있는 데이터들을 시각화   
![lead_desc_length1](/img/lead_desc_length1.png)
![lead_desc_length2](/img/lead_desc_length2.png)  
>>--> lead_desc_length 값이 3인 데이터들은 영업 전환 성공 비율이 주위 데이터에 비해 높은 편  
--> lead_desc_length 값이 14인 데이터들은 영업 전환 성공 비율이 매우 낮음  
 __&xrarr; lead_desc_length 컬럼의 결측치가 전혀 없는 것을 고려하여 값이 정확한 특징이 파악되지 않는 3, 14 값을 결측치 취급__ _(median 값으로 대체)_  
>
><br>

>lead_desc_length의 분포 확인  
>
>![lead_desc_length3](/img/lead_desc_length3.png)  
>>--> 데이터가 왼쪽으로 쏠림  
__&xrarr; 분포 변환 적용 고려__  
>
><br>

>value_counts 값이 20개 이상인 데이터들의 lead_desc_length(x) 별 영업 성공 비율(y) 분포 확인  
>
>![lead_desc_length4](/img/lead_desc_length4.png)  
>> --> lead_desc_length와 영업 전환 성공률은 어느정도 비례 관계가 있는 것으로 판단 가능



</details>

#

<details><summary>Validation Set</summary>

<br>

![validation_set1](/img/validation_set1.png)  

<br>

</details>

#

<details><summary>Preprocessing</summary>


### 범주형 컬럼
* __String Value Preprocess__ __&xrarr;__ _String 형식의 데이터를 통일_  
Ex) End / Customer, End-customer, end_Customer --> endcostumer   
![str_value_preprocess](/img/str_value_preprocess.png)  

<br>  
<br>


* __Encoding__
    * [customer_type, customer_position, expected_timeline] 컬럼    
    실제 구매 페이지에서 활용되는 항목만 Encoding, 나머지는 Others 취급  
    ![encoding_help](/img/encoding_help.png)  <br>  <br>
    * [customer_idx] 컬럼  
    ![pre_customer_idx](/img/pre_customer_idx.png)  <br>  <br>
    * 나머지 컬럼  
    customer_idx 컬럼과 마찬가지로 value_counts 값이 일정 값 이상인 값들만 인코딩 진행  

<br>


### 수치형(연속형) 컬럼
* __lead_desc_length 컬럼__  
  ![pre_lead_desc_length1](/img/pre_lead_desc_length1.png)  
    __&xrarr;__ 기존에 이상치로 판단한 3과 14를 결측치로 취급 (median 값으로 대체)  
<br>
<br>

  ![pre_lead_desc_length2](/img/pre_lead_desc_length2.png)  
    __&xrarr;__ Boxcox를 이용한 분포 변환  

<br>
<br>

* __historical_existing_cnt__   
lead_desc_length 컬럼과 마찬가지로 분표 변환  


</details>

#

<details><summary>Modeling</summary>

### EDA시 얻은 정보를 바탕으로 서로 다른 모델 두 가지 구축 (customer_type컬럼 학습 여부)  

<br>

* __customer_type 컬럼을 학습하지 않는 Train Model__  
Threshold 별로 F1-score, Recall 계산 후 3*F1-score + Recall 값이 가장 큰 Threshold로 Val_Set을 예측    
![modeling1](/img/modeling1.png)

<br>
<br>


각 Threshold 별 Train_Set의 지표값 평균과 Val_Set의 지표값 시각화  
![modeling2](/img/modeling2.png)  
__&xrarr;__ _Best Threshold : 0.15, 이때 F1-score : 0.563 Recall : 0.769_  
__&xrarr;__ __val_set_result.csv 저장__  

<br>  
<br>
<br>


* __customer_type 컬럼을 학습하는 CT_Train Model__  
Threshold 별로 F1-score, Recall 계산 후 3*F1-score + Recall 값이 가장 큰 Threshold로 CT_Val_Set을 예측  
![modeling3](/img/modeling3.png)

<br>
<br>


각 Threshold 별 Train_Set의 지표값 평균과 Val_Set의 지표값 시각화  
![modeling4](/img/modeling4.png)  
__&xrarr;__ _Best Threshold : 0.2, 이때 F1-score : 0.593 Recall : 0.672_  
__&xrarr;__ __ct_val_set_result.csv 저장__  


</details>

#

<details><summary>Ensemble</summary>


### 영업 전환 가능성이 조금이라도 있는 고객을 찾기 위해 두 가지 결과 중 하나라도 True면 True로 예측  
![ensemble1](/img/ensemble1.png)  


<br>
<br>
<br>


* 최종 예측 값에 대한 평가 지표  
![ensemble2](/img/ensemble2.png)  
__&xrarr;__ __기존 F1-score : 0.563, Recall : 0.769 에서 F1-score:0.566, Recall : 0.800으로 F1,Recall값 모두 상승__ 


</details>

#

<details><summary>Result</summary>

* .

</details>

#
