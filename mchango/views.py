from .models import ContributionPage, Status
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import ContributionPageForm, PledgeForm
from django.views.decorators.http import require_POST

# Create your views here.
@login_required
def index(request):
    pages = ContributionPage.objects.filter(user=request.user) | ContributionPage.objects.filter(pledges__user=request.user) | ContributionPage.objects.filter(transactions__user=request.user)
    pages = pages.distinct()
    context = {
        'title': 'Contribution Pages',
        'pages': pages
    }
    return render(request, 'fundly/index.html', context)

@login_required
def dashboard(request, pk, slug):
    try:
        page = ContributionPage.objects.get(slug=slug, id=pk)
        context = {
            'title': f"{page.getId()} Dashboard",
            'page': page
        }
        return render(request, 'fundly/dashboard.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "The requested page was not found.")
        return redirect('mchango:index')
    except Exception as e:
        messages.error(request, "An unexpected error occurred. Please try again later.")
        print(f"Error in dashboard view: {e}") 
        return redirect('mchango:index')

@login_required
def contribute(request, slug):
    try:
        page = ContributionPage.objects.get(slug=slug, status__name='Active')
        form = PledgeForm()
        context = {
            'title': f"Contribute to Page {page.getId()}",
            'page': page,
            'form': form
        }
        return render(request, 'fundly/contribute.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "The requested page is not available.")
        return redirect('mchango:index')
    except Exception as e:
        messages.error(request, "An unexpected error occurred. Please try again later.")
        print(f"Error in contribute view: {e}")
        return redirect('mchango:index')

@login_required
def create(request):
    form = ContributionPageForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            page = form.save(commit=False)
            page.user = request.user
            page.status = Status.objects.get(name='Pending')
            page.save()
            messages.success(request, f"{page.getId()} has been created successfully, pending approval.")
            return redirect('mchango:dashboard', pk=page.id, slug=page.slug)
        else:
            messages.error(request, "An error occurred. Please correct the errors below.")

    context = {
    'title': 'Create Contribution Page',
        'description': f'''
            Welcome {request.user.first_name}! This is where you can set up a new fundraising campaign to support your cause, project, or initiative. 
            Whether you're raising funds for medical expenses, education, community projects, or any other purpose, this tool makes it easy to get started.

            Here’s what you’ll need to do:
            1. Set a Goal & Pupose: Define how much money you need to raise and by when. Be clear and realistic about your target amount and deadline.
            2. Tell Your Story: Write a compelling description of your cause. Explain why it matters and how the funds will be used. Use images or videos to make your page more engaging.
            5. Publish and Share: Once your page is ready, publish it and share the link with your network to start receiving contributions.

            Tips for Success:
            - Be transparent about how the funds will be used.
            - Regularly update your contributors on the progress of your campaign.
            - Promote your page on social media, email, and other channels to reach a wider audience.

            Thank you for choosing Fundly to support your cause. Let’s make a difference together!
        ''',
        'form': form
    }
    return render(request, 'fundly/create.html', context)
    
@login_required
def edit(request, pk, slug):
    try:
        page = ContributionPage.objects.get(slug=slug, id=pk)
        if not request.user.is_staff and not request.user.is_superuser and page.user != request.user:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('mchango:dashboard', pk=pk, slug=slug)
        
        form = ContributionPageForm(request.POST, request.FILES, instance=page)

        if request.method == 'POST':
            if form.is_valid():
                page = form.save(commit=False)
                page.status = Status.objects.get(name='Pending')
                page.save()
                messages.success(request, f"{page.getId()} has been updated.")
                return redirect('mchango:dashboard', pk=pk, slug=slug)
            else:
                messages.error(request, "An error occurred. Please correct the errors below.")
        return render(request, 'fundly/create.html', {
            'title': f'Edit {page.getId()}',
            'description': '''
                Welcome to the Contribution Page Editor! This is where you can update and refine your existing fundraising campaign to ensure it continues to attract support and achieve its goals. 
                Whether you need to adjust your target amount, update your story, or add new visuals, this tool makes it easy to keep your campaign fresh and engaging.

                Here’s what you can do:
                1. Update Your Goal: Adjust your target amount or deadline if needed. Keep your contributors informed about any changes.
                3. Edit Details: Modify essential information such as the purpose of the campaign, contact person, or additional notes for contributors.
                5. Review and Save: Once you’ve made your updates, save the changes and let your contributors know about the improvements.

                Tips for Success:
                - Keep your contributors informed about any changes to your campaign.
                - Use high-quality visuals and compelling updates to maintain interest.
                - Promote your updated page on social media, email, and other channels to reach a wider audience.

                Thank you for using Fundly to support your cause. Your dedication makes a difference!
            ''',
            'form': form
            })
    except ObjectDoesNotExist:
        messages.error(request, "The requested page was not found.")
        return redirect('mchango:index')
    except Exception as e:
        messages.error(request, "An unexpected error occurred. Please try again later.")
        print(f"Error in edit view: {e}")
        return redirect('mchango:index')

#change status
@login_required
def change_status(request, pk, slug):
    try:
        page = ContributionPage.objects.get(slug=slug, id=pk)
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('mchango:dashboard', pk=pk, slug=slug)
        
        if request.method == 'POST':

            pass
        else:
            context = {
                'title': f"Change Status of {page.getId()}",
                'page': page
            }
            return render(request, 'fundly/change_status.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "The requested page was not found.")
        return redirect('mchango:index')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred. Please try again later.\n{e}")
        print(f"Error in change_status view: {e}")
        return redirect('mchango:index')
    
#close
@login_required
def close(request, pk, slug):
    try:
        page = ContributionPage.objects.get(slug=slug, id=pk)
        if not request.user.is_staff and not request.user.is_superuser and page.user != request.user:
            messages.error(request, "You do not have permission to perform this action.")
            return redirect('mchango:dashboard', pk=pk, slug=slug)
        
        page.status = Status.objects.get(name='Closed')
        page.save()
        messages.success(request, f"{page.getId()} has been closed.")
        return redirect('mchango:dashboard', pk=pk, slug=slug)
    except ObjectDoesNotExist:
        messages.error(request, "The requested page was not found.")
        return redirect('mchango:index')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred. Please try again later.\n{e}")
        print(f"Error in close view: {e}")
        return redirect('mchango:index')
    
@login_required
@require_POST
def store_pledge(request, slug):
    try:
        form = PledgeForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                pledge = form.save(commit=False)
                pledge.user = request.user
                pledge.balance = pledge.amount
                pledge.page = ContributionPage.objects.get(slug=slug)
                pledge.save()
                messages.success(request, "Your pledge has been received.")
                return redirect('mchango:dashboard', pk=pledge.page.id, slug=pledge.page.slug)
            else:
                messages.error(request, "An error occurred. Please correct the errors below.")
                return redirect('mchango:contribute', slug)
    except ObjectDoesNotExist:
        messages.error(request, "The requested page is not available.")
        return redirect('mchango:index')
    except Exception as e:
        messages.error(request, f"Error. {e}!")
        print(f"Error in store_pledge view: {e}")
        return redirect('mchango:contribute', slug)