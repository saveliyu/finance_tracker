from django.shortcuts import render

# Create your views here.
def family_view(request):
    family_members = list()
    if request.user.family_members:
        family_members = request.user.family_members.all()
    context = {
        'family_members': family_members,
    }
    return render(request, 'family/family.html', context)