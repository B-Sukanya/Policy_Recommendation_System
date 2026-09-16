# InsurAI Policy Recommendation POC

A client-demo Streamlit application for **Policy Recommendation (Insurance)**. It supports a real product catalogue upload and a transparent scoring layer to show how customer needs can be turned into explainable recommendations.

## Run locally

```powershell
cd C:\demo-usecases
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run app.py
```

The application opens at `http://localhost:8501`.

## Demo flow

1. Adjust the customer profile in the recommendation studio.
2. Upload one or more CSV or Excel product catalogues together in the sidebar. The files are combined into one catalogue. Required columns are:
   `plan_name`, `monthly_premium`, `annual_coverage`, `deductible`, and `network`.
3. Show how budget, coverage preference, family context and digital/wellness preferences change the ranking.
4. Explain the recommended plan using the rationale and comparison cards.
5. Download the recommendation summary.

If no catalogue is uploaded, the app clearly labels and uses its synthetic fallback catalogue. Product terms, pricing, eligibility, underwriting, audit logging and approved customer data integrations should be added before production use. Do not use production secrets in a demo environment.
