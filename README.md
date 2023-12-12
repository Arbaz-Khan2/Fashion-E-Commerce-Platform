# Fashion-E-Commerce-Platform
User Authentication
	To register, you need to provide the necessary details. Subsequently, you can log in by entering your username and password, obtaining a token that will be used for authentication purposes.
Register User
Endpoint: /register/
Method: POST
Header:
Description: Register a new user.
Request:
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "secure_password",
  "profile": {
    "phone": "1234567890", // your mobile number
    "address": "your address"
  },
  "role": "your_role" // admin, staff, customers
}
Login User
Endpoint: /login/
Method: POST
Header:
Description: Log in an existing user.
Request:
{
  "username": "example_user",
  "password": "secure_password"
}
User Profile
Endpoint: /profile/
Method: GET (Get user profile) | PUT (Update user profile)
Header: key = Authorization, value = Token your_token
Description: Get or update the user's profile.
Request (GET): // no need to add the any data just pass the token to headers
Request (PUT):
{
  "phone": "9876543210", // your updated mobile number
  "address": " your updated address"
}
Product Catalog
You can execute CRUD operations for categories, brands, and products. It's possible to add numerous categories and brands directly to the database. When adding a product, valid category and brand IDs must be provided, indicating that a category and brand must exist in the database before adding a product.
Manage Category
Endpoint: http://product-catalog/categories/
Method: GET (Get all categories) | POST (Create a new category) | PUT (Update a category) | DELETE (Delete a category)
Header: key = Authorization, value = Token admin_or_staff_token 
Description: Get all categories, create a new category, update, or delete an existing category.
Request (POST):
{
  "name": "your_category"
}
Request (GET): // no need to add the any data.
Request (PUT):
{
"id": 1, // id of the category
  "name": "your_updated_category"
}
Request (DELETE):
{
"id": 1, // id of the category
}
Manage Brand
Endpoint: /product-catalog/brands/
All other functionalities mirror those of the category.
Manage Product
Endpoint: /product-catalog/products/
Method: GET (Get all products) | POST (Create a new product) | PUT (Update a product) | DELETE (Delete a product)
Header: key = Authorization, value = Token admin_or_staff_token 
Description: Get all products, create a new product, update, or delete an existing product.
Request (POST):
{
  "name": "product_name",
  "description": "some_discription_of_product",
  "category_id": 1, // id should be in the database
  "brand_id": 1, // id should be in the database
  "price": 799.99,
  "inventory": 50,
  "attributes": [
    {
      "name": " attribute_name",
      "value": " attribute_value"
    }
// you can add as many attributes as you want in this list
  ]
}
Request (GET): // no need to add the any data.
Request (PUT): // same as POST just add the id of the product.
Request (DELETE):
{
"id": 1, // id of the product
}
Get Suggestions
	You can retrieve product suggestions, encompassing items from your historical searches and previous orders.
Endpoint: /suggestions/
Method: GET
Header: key = Authorization, value = Token customer_token 
Description: Get product suggestions based on user search history and previous orders.
Request (GET): // no need to add the any data.
Shopping Cart
	You can add products to your shopping cart, maintaining the cart's current state for potential modifications. During the checkout process, you need to supply the transaction ID for the payment and the chosen payment method. Subsequently, an order will be generated for all items in the cart, saving it for future reference. Furthermore, the inventory of purchased products will be reduced.
Manage Cart
Endpoint: /cart/
Method: GET (Get user's shopping cart) | POST (Add product to cart) | DELETE (Delete user's shopping cart)
Header: key = Authorization, value = Token customer_token
Description: Get the user's shopping cart, add a product to the cart, or delete the entire cart. 
Request (POST):
{
  "product_id": 1
}
Request (GET): // no need to add the any data.
Request (DELETE): // no need to add the any data. It will get the user from request and will delete that user’s cart.
Checkout
Endpoint: /checkout/
Method: POST
Header: key = Authorization, value = Token customer_token
Description: Checkout and place an order.
Request (POST):
{
  "transaction_id": "txn_id",
  "payment_method": "payment_method"
}
Orders
	You can check your order history any time.
Endpoint: /orders/
Method: GET
Header: key = Authorization, value = Token customer_token
Description: Get a list of orders placed by the user.
Request (DELETE): // no need to add the any data. It will get the user from request and will return that user’s order.
Reviews
	Customers have the option to add reviews and ratings for their orders after completing the checkout process. These reviews are then accessible to all other users on the platform, providing transparency and insight into the experiences shared by customers.
Add Review
Endpoint: /add_review/
Method: POST
Header: key = Authorization, value = Token customer_token
Description: Add a review for a specific order.
Request (POST):
{
  "order_id": 1,
  "rating": 5,
  "review": "Great product, fast delivery!"
}
Get Reviews
Endpoint: /reviews/
Method: GET
Header: key = Authorization, value = Token your_token
Description:
Get a list of all reviews. 
Request (GET): // no need add any data.
Search History
Get Search History
Endpoint: /search_history/
Method: GET
Description: Get a list of search keywords used by the user.
Request (GET): // no need add any data.
Advanced Search and Filtering
	Users can apply advanced search filters to refine their product searches. Parameters can be included in the request to filter products, but it's important to note that all parameters are optional. If no parameters are provided, the system will return all available products.
Endpoint: /product-catalog/products/
Method: GET
Header: key = Authorization, value = Token your_token
Parameters:
keyword: some_key_word
category_id: some_category_id
brand_id: some_brand_id
min_price: some_value
max_price: some_vlaue
Description:
Get a list of all reviews. 
Request (GET): // no need add any data.
