from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from .models import Product,Comments
from django.http import HttpResponse
from django.shortcuts import redirect,render,get_object_or_404
from .forms import ProductForm,commentform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'myapp/home.html', {'user': request.user})


@login_required
def dashboard(request):
    messages.info(request, "📢 You’ve reached the dashboard view.")
    user=request.user
    products=Product.objects.filter(user=user)
    if products.exists():
        return render(request,'myapp/dashboard.html',{'products':products})
    else:
        return redirect('product_create')
        #return render(request,'myapp/dashboard.html',{'products':products,'message':'No products found.'})
    

def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            print(f"Username: {username}, Password: {password}")
            user=authenticate(username=username,password=password)
            print(f"Authenticated user: {user}")
            login(request,user)
            messages.success(request, f"🎉 Welcome, {username}! You’re now signed in.")
            return redirect(reverse('dashboard'))
    else:
        form=UserCreationForm()
    return render(request,'myapp/signup.html',{'form':form})
        

def product_list(request):
    products=Product.objects.all()
    return render(request,'myapp/index.html',{'products':products})

def product_detail(request,pk):
    print(">>> ENTERED PRODUCT DETAIL VIEW <<<")  # Debug 
    product = get_object_or_404(Product, pk=pk)
    #Access control
    if not(product.user==request.user or request.user in product.shared_with.all()):
        return HttpResponseForbidden("you are not allowed to view this product.")
    comments=product.comments.all()
    print("Comments count:", comments.count())
    #print("Comments count:", comments.count())
    if request.method=='POST':
        form=commentform(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.product=product
            comment.save()
            return redirect('product_detail',pk=product.pk)
    else:
        form=commentform()
    return render(request,'myapp/index2.html',{
        'product':product,
        'comments':comments,
        'form':form,
    })

    #Product=Product.objects.get(pk=pk)
    #return render(request,'myapp/index2.html',{'product':product})
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product = form.save(commit=False)
            Product.user = request.user
            Product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'myapp/productcreate.html', {'form': form})
@login_required
def edit_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if product.user!=request.user:
        return HttpResponse("You are not allowed to edit this product.")
    if request.method=='POST':
        form=ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form=ProductForm(instance=product)
    return render(request,'myapp/edit.html',{'form':form})
@login_required   
def delete_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if product.user!=request.user:
        return HttpResponse("You are not allowed to delete this product.")
    if request.method=='POST':
        product.delete()
        return redirect('product_list')
    return render(request,'myapp/delete.html',{'product':product})

@login_required
def edit_comment(request,comment_id):
    comment=get_object_or_404(Comments,pk=comment_id)
    if request.method=='POST':
        form=commentform(request.POST,instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comments',product_id=comment.product.pk)
    else:
        form=commentform(instance=comment)
    return render(request,'myapp/editcomment.html',{'form':form})
@login_required
def delete_comment(request,comment_id):
    comment=get_object_or_404(Comments,pk=comment_id)
    if request.method=='POST':
        comment.delete()
        return redirect('comments',product_id=comment.product.pk)
    return render(request,'myapp/deletecomment.html',{'comment':comment})
@login_required
def comments(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    comments=product.comments.all()
    return render(request,'myapp/index2.html',{
        'product':product,
        'comments':comments,
    })

@login_required
def share_product(request, pk):
    Product=get_object_or_404(Product, pk=pk)
    if Product.user != request.user:
        return HttpResponseForbidden("You can’t share someone else's post!")
    if request.method == 'POST':
        username=request.POST.get('username')
        try:
            user_to_share =User.objects.get(username=username)
            Product.shared_with.add(user_to_share)
            messages.success(request, f"shared with {username}")
        except User.DoesNotExist:
            messages.error(request,f'No user names {username}')
    return redirect('product_detail',pk=pk)

