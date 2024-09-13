import os, requests

def get_chargebee_subscriptions(company_id, custom_object_type_id, headers, base_url):
    url = f'{base_url}/crm/v3/objects/companies/{company_id}/associations/{custom_object_type_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return None

def main(event):
  cId = event.get('inputFields').get('hs_object_id')
  token = os.getenv("RevOps")
  chargebeeID = '2-14800898'
  headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
  }
  base_url = 'https://api.hubapi.com'
  subscriptions = get_chargebee_subscriptions(cId, chargebeeID, headers, base_url)
  subIds = [subscription['id'] for subscription in subscriptions]
  actTaxSubDetails = []
  for i in subIds:
    url = f'{base_url}/crm/v3/objects/{chargebeeID}/{i}?properties=plan_name,status'
    response = requests.get(url, headers=headers)
    properties = (response.json()).get('properties',{})
    plan_name = properties.get('plan_name')
    status = properties.get('status')
    if(status == 'active' and plan_name != None):
      if 'Tax' in plan_name or 'tax' in plan_name:
        actTaxSubDetails.append(plan_name)
  taxPlans = ", ".join(actTaxSubDetails)
  return {
    "outputFields": {
      "TaxPlans": taxPlans
    }
  }