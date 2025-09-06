import os
import requests

from queries import get_products, update_variant_price, staged_uploads_create, run_bulk_operation_mutation, get_current_bulk_operation

class Shopify():

  def get_products(self, collection_id, after_cursor):
    params = {
      "query": "collection_id:" + str(collection_id)
    }
    if after_cursor: params["after"] = after_cursor
    return self.execute(get_products, params).json()["data"]["products"]
  
  def get_product_jsonl(self, product_id, variant_id, new_price):
    return {
      "productId": product_id,
      "variants": [{
        "id": variant_id,
        "price": new_price,
      }]
    }
  
  def create_staged_upload(self):
    return self.execute(staged_uploads_create, {}).json()
  
  def upload_jsonl(self, url, parameters):
    form_data = { param["name"]: param["value"] for param in parameters }
    form_data["file"] = open("/tmp/price_updates.jsonl", "r")
    requests.post(url, files=form_data)
    return form_data["key"]
  
  def run_bulk_operation_mutation(self, stage_upload_path):
    return self.execute(run_bulk_operation_mutation, {
      "mutation": update_variant_price,
      "stagedUploadPath": stage_upload_path
    })

  def get_current_bulk_operation(self):
    return self.execute(get_current_bulk_operation, {}).json()

  def get_headers(self):
    return {
      "Content-Type": "application/json",
      "X-Shopify-Access-Token": os.environ.get("SHOPIFY_ACCESS_TOKEN")
    }

  def execute(self, query, variables):
    return requests.post(os.environ.get("SHOPIFY_ADMIN_API_URL"), json={"query": query, "variables": variables}, headers=self.get_headers())
  