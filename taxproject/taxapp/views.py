from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import IncomeForm
from .models import TaxRecord
from decimal import Decimal # <-- Decimal ইম্পোর্ট করা আছে কিনা নিশ্চিত হোন

# রেজিস্ট্রেশন
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'taxapp/register.html', {'form': form})

# লগইন
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'taxapp/login.html', {'form': form})

# লগআউট
def user_logout(request):
    logout(request)
    return redirect('login')

# ==========================================================
# ===== START OF MODIFIED DASHBOARD VIEW =================
# ==========================================================
@login_required
def dashboard(request):
    context = {}
    
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.cleaned_data['annual_income']
            
            # tax_data এখন একটি ডিকশনারি
            tax_data = calculate_tax(income) 
            
            # ডেটাবেসে সেভ করুন
            TaxRecord.objects.update_or_create(
                user=request.user,
                defaults={
                    'annual_income': income, 
                    'calculated_tax': tax_data['total_tax']
                }
            )
            
            # সব তথ্য context এ যোগ করুন
            context['total_yearly_income'] = income
            context['tax_free_allowance'] = tax_data['tax_free_allowance']
            context['taxable_income'] = tax_data['taxable_income']
            context['total_tax_payable'] = tax_data['total_tax']
            context['form'] = form # ফর্মটি পেজে আবার দেখান
            
            # সাবমিট করার পর রেজাল্ট দেখান (redirect না করে)
            return render(request, 'taxapp/dashboard.html', context)
    
    # এটি GET রিকোয়েস্ট হ্যান্ডেল করবে (পেজ প্রথমবার লোড হলে)
    form = IncomeForm()
    record = TaxRecord.objects.filter(user=request.user).first()
    
    if record:
        # যদি পুরোনো রেকর্ড থাকে, তবে সেই অনুযায়ী সব তথ্য দেখান
        tax_data = calculate_tax(record.annual_income)
        
        context['total_yearly_income'] = record.annual_income
        context['tax_free_allowance'] = tax_data['tax_free_allowance']
        context['taxable_income'] = tax_data['taxable_income']
        context['total_tax_payable'] = record.calculated_tax
        
        # ফর্মটি পুরোনো তথ্য দিয়ে পূরণ করুন
        form = IncomeForm(initial={'annual_income': record.annual_income})

    context['form'] = form
    return render(request, 'taxapp/dashboard.html', context)
# ==========================================================
# ===== END OF MODIFIED DASHBOARD VIEW ===================
# ==========================================================


# ==========================================================
# ===== START OF MODIFIED TAX CALCULATION FUNCTION =======
# ==========================================================
def calculate_tax(income):
    # 'income' একটি Decimal অবজেক্ট
    
    # ট্যাক্স-ফ্রি অ্যালাউন্স গণনা
    tax_free_option1 = income / Decimal('3')
    tax_free_option2 = Decimal('450000')
    tax_free_allowance = min(tax_free_option1, tax_free_option2)

    # ট্যাক্সেবল ইনকাম গণনা
    taxable_income = max(income - tax_free_allowance, Decimal('0'))

    # ট্যাক্স স্ল্যাব (Decimal ব্যবহার করে)
    slabs = [
        (Decimal('350000'), Decimal('0.00')),
        (Decimal('100000'), Decimal('0.05')),
        (Decimal('400000'), Decimal('0.10')),
        (Decimal('500000'), Decimal('0.15')),
        (None,              Decimal('0.20'))
    ]

    remaining_income = taxable_income
    total_tax = Decimal('0.0')

    # ট্যাক্স গণনা
    for slab_amount, slab_rate in slabs:
        if remaining_income <= 0:
            break
        if slab_amount is not None:
            income_in_slab = min(remaining_income, slab_amount)
        else:
            income_in_slab = remaining_income
        
        total_tax += income_in_slab * slab_rate 
        remaining_income -= income_in_slab

    # সব তথ্যসহ একটি ডিকশনারি রিটার্ন করুন
    return {
        'total_tax': total_tax,
        'taxable_income': taxable_income,
        'tax_free_allowance': tax_free_allowance
    }
# ==========================================================
# ===== END OF MODIFIED TAX CALCULATION FUNCTION =========
# ==========================================================


def homepage_view(request):
    return render(request, 'taxapp/homepage.html')