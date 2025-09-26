[React UploadForm] 


   ↓ (이미지 3개 업로드)

   
POST /api/solutions/analyze/


   ↓

   
[views.py: SolutionAnalysisView]
   - 이미지 저장
   - GPT API 호출 (services.py)
   - 응답 DB 저장
   - 응답 반환

     
   ↓

   
[serializers.py: SolutionAnalysisSerializer]
   - DB 객체 → JSON 직렬화

     
   ↓ 


[React ResultView]
   - gpt_response 표시
