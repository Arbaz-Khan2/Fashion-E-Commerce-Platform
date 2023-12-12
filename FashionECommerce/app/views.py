from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile, Category, Brand, Attribute, Product, CartItem, Cart, Payment, OrderItem, Order, Review, SearchHistory
from .serializers import UserSerializer, UserProfileSerializer, CategorySerializer, BrandSerializer, AttributeSerializer, ProductSerializer, CartItemSerializer, CartSerializer, PaymentSerializer, OrderItemSerializer, OrderSerializer, ReviewSerializer, SearchHistorySerializer
from .permissions import IsAdminOrStaffPermission, IsCustomerPermission
from django.db.models import Q
from django.db import transaction

# this function handles the user registration
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Token.objects.create(user=user)
        return Response({'message': 'User registered successfully'})
    return Response(serializer.errors, status=400)

# this function handles the user login and returns the token
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)

# this function handles profile update and retrieval
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def manage_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # if method is GET, return the profile data
    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
    # if method is PUT, update the profile data
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=400)

# this function handles the category creation, updation and retrieval
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsAdminOrStaffPermission])
def manage_category(request):

    # if method is GET, return all the categories
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    # if method is POST, create a new category
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # if method is PUT, update the category
    elif request.method == 'PUT':
        category = Category.objects.get(id=request.data.get('id'))
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # if method is DELETE, delete the category
    elif request.method == 'DELETE':
        category = Category.objects.get(id=request.data.get('id'))
        category.delete()
        return Response({'message': 'Category deleted successfully'})

# this function handles the brand creation, updation and retrieval
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsAdminOrStaffPermission])
def manage_brand(request):

    # if method is GET, return all the brands
    if request.method == 'GET':
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)
    
    # if method is POST, create a new brand
    elif request.method == 'POST':
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # if method is PUT, update the brand
    elif request.method == 'PUT':
        brand = Brand.objects.get(id=request.data.get('id'))
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # if method is DELETE, delete the brand
    elif request.method == 'DELETE':
        brand = Brand.objects.get(id=request.data.get('id'))
        brand.delete()
        return Response({'message': 'Brand deleted successfully'})

# this function handles the product creation, updation, retrieval and advanced search filters
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsAdminOrStaffPermission])
def manage_product(request):

    # if method is GET, filter the products based on the query parameters and return the results
    if request.method == 'GET':
        products = Product.objects.all()
        keyword = request.query_params.get('keyword', '')
        category_id = request.query_params.get('category_id', '')
        brand_id = request.query_params.get('brand_id', '')
        min_price = request.query_params.get('min_price', '')
        max_price = request.query_params.get('max_price', '')
        if keyword:
            products = products.filter(
                Q(name__icontains=keyword) |
                Q(description__icontains=keyword),
            )
            search_history, created = SearchHistory.objects.get_or_create(user=request.user, keyword=keyword)
            search_history.save()
        if category_id:
            products = products.filter(category_id=category_id)
        if brand_id:
            products = products.filter(brand_id=brand_id)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    # if method is POST, create a new product and add its attributes
    elif request.method == 'POST':
        product_data = request.data.copy()
        attributes_data = product_data.pop('attributes', [])
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            product = serializer.save()
            for attribute_data in attributes_data:
                attribute_name = attribute_data.get('name')
                attribute_value = attribute_data.get('value')
                attribute = Attribute.objects.create(name=attribute_name, value=attribute_value, product=product)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # if method is PUT, update the product and update the attributes
    elif request.method == 'PUT':
        product = Product.objects.get(id=request.data.get('id'))
        product_data = request.data.copy()
        attributes_data = product_data.pop('attributes', [])
        serializer = ProductSerializer(product, data=product_data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            attributes = Attribute.objects.filter(product=product)
            attributes.delete()
            for attribute_data in attributes_data:
                attribute_name = attribute_data.get('name')
                attribute_value = attribute_data.get('value')
                attribute = Attribute.objects.create(name=attribute_name, value=attribute_value, product=product)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # if method is DELETE, delete the product, it will delete the attributes as well
    elif request.method == 'DELETE':
        product = Product.objects.get(id=request.data.get('id'))
        product.delete()
        return Response({'message': 'Product deleted successfully'})

# this function handles the cart creation, updation and retrieval
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsCustomerPermission])
def manage_cart(request):

    # if method is GET, return the cart data
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # if method is POST, add the product to the cart or if product is already there then update the its quantity
    elif request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        try:
            product = Product.objects.get(id=request.data.get('product_id'))
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data)
    
    # if method is DELETE, delete the product from the cart
    elif request.method == 'DELETE':
        cart = Cart.objects.get(id=request.data.get('id'))
        cart.delete()
        return Response({'message': 'Cart deleted successfully'})

# this function handles the checkout process
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsCustomerPermission])
def checkout(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    if cart.cartitem_set.count() == 0:
        return Response({'detail': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # perform all actions as atomic if any one fail then do not make any change in the database
        with transaction.atomic():
            transaction_id =  request.data.get('transaction_id')
            payment_method =  request.data.get('payment_method')
            payment = Payment.objects.create(transaction_id=transaction_id, payment_method=payment_method)
            order = Order.objects.create(user=user, payment=payment)
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                )
                cart_item.product.inventory -= cart_item.quantity
                cart_item.product.save()
            order_serializer = OrderSerializer(order)
            cart.cartitem_set.all().delete()
            cart.delete()
        return Response(order_serializer.data)
    except Exception as e:
        return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

# this function handles the order retrieval
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsCustomerPermission])
def get_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# this function handles the review creation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, IsCustomerPermission])
def add_review(request):
    user = request.user
    order_id = request.data.get('order_id')
    rating = request.data.get('rating')
    review = request.data.get('review')
    try:
        order = Order.objects.get(id=order_id, user=user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    review = Review.objects.create(order=order, rating=rating, review=review)
    review_serializer = ReviewSerializer(review)
    return Response(review_serializer.data)

# this function handles the review retrieval
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_reviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# this function handles the search history retrieval
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_search_history(request):
    search_history = SearchHistory.objects.filter(user=request.user)
    serializer = SearchHistorySerializer(search_history, many=True)
    return Response(serializer.data)

# this function handles the suggestions retrieval
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_seggestions(request):
    keywords = SearchHistory.objects.filter(user=request.user).values_list('keyword', flat=True)
    products = Product.objects.filter(name__in=keywords)
    previous_order_products = Product.objects.filter(
        orderitem__order__user=request.user, orderitem__order__payment__isnull=False, orderitem__order__payment__transaction_id__isnull=False)
    products = products.union(previous_order_products)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
