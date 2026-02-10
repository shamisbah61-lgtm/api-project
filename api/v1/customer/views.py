from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from customer.models import Category
from .serializers import CategorySerializer
from user.models import User 
from customer.models import Product
from .serializers import ProductSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        response_data ={
            "status_code":201,
            "status":"error",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "message":"login successful"
        }
        return Response(response_data)
    else:
        response_data={
            "status_code":400,
            "status":"error",
            "message":"login not found"
        }
        return Response(response_data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email).exists():
        response_data = {
            "status_code": 400,
            "status": "error",
            "message": "User with this email already exists."
        }
        return Response(response_data)
    else:
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
    response_data = {
        "status_code": 201,
        "status": "success",
        "message": "User registered successfully."
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories(request):
  
    categories = Category.objects.all()
    context={
        "request":request

    }
    serializers = CategorySerializer(categories,many=True,context=context)
    response_data = {
        "status_code":200,
        "data":serializers.data,

        "message":"category sucessfull"
    }
    return Response(response_data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
    name = request.data.get("name")

   

    category = Category.objects.create(
        user=request.user,
        name=name
    )

    serializer = CategorySerializer(
        category,
        context={"request": request}
    )

    return Response({
        "status_code": 201,
        "status": "success",
        "message": "Category created successfully",
        "data": serializer.data
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_category(request, id):
    user=request.user
    category = Category.objects.get(id=id ,  user = user)
    name = request.data.get("name")
    
    

    category.name = name
    category.save()
    serializer = CategorySerializer(category,context={"request":request})
    response_data  = {
        "status_code":201,
         "status":"succes",
         "message":"edit successfully",
         "data":serializer.data

    }
    return Response(response_data)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, id):
    user = request.user
    category = Category.objects.get(id=id , user=user)
    category.delete()

    response_data = {
        "status_code":200,
        "status":"deleted",
        "message":"delete successfully",
        "data":{}

    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product(request):
    product = Product.objects.all()
    context={
        "request":request

    }
    serializers = ProductSerializer(product,many=True,context=context)
    response_data = {
        "status_code":200,
        "data":serializers.data,

        "message":"product sucessfull"
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    name =request.data.get("name")

    product = Product.objects.create(
        user = request.user,
        name=name
    )

    serializer = ProductSerializer(
        product,
        context={"request": request}
    )
    return Response({
        "status_code": 201,
        "status": "success",
        "message": "product added successfully",
        "data": serializer.data
    })
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_product(request, id):
    user = request.user
    product = Product.objects.get(id=id,  user = user)
    name = request.data.get("name")


    product.name = name
    product.save()
    serializer = ProductSerializer(product,context={"request":request})
    response_data  = {
        "status_code":201,
         "status":"succes",
         "message":"edit successfully",
         "data":serializer.data

    }
    return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, id):
    user = request.user
    product = Product.objects.get(id=id , user=user)
    product.delete()

    response_data = {
        "status_code":200,
        "status":"deleted",
        "message":"delete successfully",
        "data":{}

    }
    return Response(response_data)
