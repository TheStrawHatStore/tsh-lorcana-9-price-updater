get_products = '''
  query products($query: String, $after: String) {
    products(first: 50, after: $after, query: $query) {
      nodes {
        id
        title
        handle
        metafields(first: 10, keys: ["custom.number", "custom.rarity"]){
          nodes {
            id
            key
            value
          }
        }
        variants(first: 10) {
          nodes {
            id
            title
            price
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
'''

staged_uploads_create="""
  mutation {
    stagedUploadsCreate(input:{
      resource: BULK_MUTATION_VARIABLES,
      filename: "price_updates",
      mimeType: "text/jsonl",
      httpMethod: POST
    }){
      userErrors{
        field,
        message
      },
      stagedTargets{
        url,
        resourceUrl,
        parameters {
          name,
          value
        }
      }
    }
  }
"""

update_variant_price = '''
  mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
    productVariantsBulkUpdate(productId: $productId, variants: $variants) {
      product {
        id
      }
      productVariants {
        id
        price
      }
      userErrors {
        field
        message
      }
    }
  }
'''

run_bulk_operation_mutation = '''
  mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!){
    bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
      bulkOperation {
        id
        url
        status
      }
      userErrors {
        message
        field
      }
    }
  }
'''

get_current_bulk_operation = '''
  query {
    currentBulkOperation(type: MUTATION) {
      id
      type
      status
      url
      partialDataUrl
    }
  }
'''