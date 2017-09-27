from django.shortcuts import render, redirect
from LonganApp.models import CareerFair
from LonganApp.models import Company
from LonganApp.models import Prefers
from LonganApp.models import Industry
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from math import sin, cos, sqrt, atan2, radians
from random import randint
from pprint import pprint

import csv
import json

def distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    if distance < 0:
        distance = -distance
    return distance

# Create your views here.
def index(request):
    return render(request, 'LonganApp/index.html', context = {
    })

def maps(request):
    return render(request, 'LonganApp/map.html', context= {
    })

def removeFromPreferences(request):
    with connection.cursor() as cursor:
        industry = request.POST['industryName']
        email = request.user.email
        cursor.execute("DELETE FROM prefers WHERE prefers.industry_name = \'" + industry + "\' AND prefers.email = \'" + email + "\'")
    return redirect("https://cs411spring2017.pythonanywhere.com/settings.html")

def addIndustryToPreferences(request):
    with connection.cursor() as cursor:
        industry = request.POST['industryName']
        email = request.user.email
        cursor.execute("INSERT INTO prefers(industry_name, email) VALUES (\'" + industry + "\', \'" + email + "\')")
    return redirect("https://cs411spring2017.pythonanywhere.com/settings.html")

def favorites(request):
    if not request.user.is_authenticated:
        return redirect("https://cs411spring2017.pythonanywhere.com/login.html")
    email = request.user.email
    company = Company.objects.raw("SELECT Company.company_id, Company.name, Company.address, Company.website FROM Company, favorites WHERE favorites.companyName = Company.name AND favorites.email = \'" + email + "\'")
    return render(request, 'LonganApp/favorites.html', context={
        'companies': company,
        'email': email
    })

def addCompanyToFavorites(request):
    email = request.user.email

    with connection.cursor() as cursor:
        company = request.POST['companyName']
        cursor.execute("INSERT INTO favorites(companyName, email) VALUES (\'" + company + "\', \'" + email + "\')")
    return redirect("https://cs411spring2017.pythonanywhere.com/company.html")

def unfavoriteCompany(request):
    with connection.cursor() as cursor:
        company = request.POST['companyName']
        email = request.user.email
        cursor.execute("DELETE FROM favorites WHERE favorites.companyName = \'" + company + "\' AND favorites.email = \'" + email + "\'")
    return redirect("https://cs411spring2017.pythonanywhere.com/favorites.html")

def settings(request):
    if not request.user.is_authenticated:
        return redirect("https://cs411spring2017.pythonanywhere.com/login.html")
    email = request.user.email
    industry = Industry.objects.raw("SELECT Industry.industry_id, Industry.name FROM Industry")
    preferred = Prefers.objects.raw("SELECT prefers.id, prefers.industry_name FROM prefers WHERE prefers.email = \'" + email + "\'")
    return render(request, 'LonganApp/settings.html', context = {
        'email': email,
        'preferred_industries': preferred,
        'industries': industry
    })

def login_view(request):
    return render(request, 'LonganApp/login.html', context = {
    })

def logoutRequest(request):
    logout(request)
    return redirect("https://cs411spring2017.pythonanywhere.com/login.html")

def loginRequest(request):
    username = request.POST['usernameLogin']
    password = request.POST['passwordLogin']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("https://cs411spring2017.pythonanywhere.com/settings.html")
    return render(request, 'LonganApp/login.html')

def signupRequest(request):
    email = request.POST['emailSignup']
    username = request.POST['usernameSignup']
    password = request.POST['passwordSignup']
    user = User.objects.create_user(username, email, password)
    if user is not None:
        login(request, user)
        return redirect("https://cs411spring2017.pythonanywhere.com/settings.html")
    return render(request, 'LonganApp/login.html')

def careerfair(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            superuser = 'true'
        else:
            superuser = 'false'
    else:
        superuser = 'false'
    careerfair = CareerFair.objects.raw('SELECT cf_id FROM CareerFair ORDER BY year')
    company = Company.objects.raw('SELECT company_id FROM Company ORDER BY name')
    return render(request, 'LonganApp/careerfair.html', context = {
        'companies': company,
        'careerfairs': careerfair,
        'filtered_by': "",
        'superuser': superuser
    })

def addCareerfair(request):
    with connection.cursor() as cursor:
        name = request.POST['name']
        year = request.POST['year']
        semester = request.POST['semester']
        location = request.POST['location']
        cursor.execute("INSERT INTO CareerFair(name, year, semester, location) VALUES (\'" + name + "\', \'" + year + "\', \'" + semester + "\', \'" + location + "\')")
    return redirect("https://cs411spring2017.pythonanywhere.com/careerfair.html")

def deleteCareerfair(request):
    with connection.cursor() as cursor:
        careerfairName = request.POST['careerfairName']
        cursor.execute("DELETE FROM CareerFair WHERE name = %s", [careerfairName])
    return redirect("https://cs411spring2017.pythonanywhere.com/careerfair.html")

def updateCareerfair(request):
    with connection.cursor() as cursor:
        name = request.POST['name']
        year = request.POST['year']
        semester = request.POST['semester']
        location = request.POST['location']
        oldName = request.POST['oldName']
        cursor.execute("UPDATE CareerFair SET name = \'" + name + "\', year = \'" + year + "\', semester = \'" + semester + "\', location = \'" + location + "\' WHERE name = \'" + oldName + "\'")
    return redirect("https://cs411spring2017.pythonanywhere.com/careerfair.html")

def filterByCareerfair(request):
    if request.user.is_authenticated:
        authenticated = 'true'
        if request.user.is_superuser:
            superuser = 'true'
        else:
            superuser = 'false'
    else:
        authenticated = 'false'
        superuser = 'false'

    careerfair_name = request.POST['careerfair']
    if not careerfair_name:
        return redirect("https://cs411spring2017.pythonanywhere.com/company.html")
    company = Company.objects.raw("SELECT Company.company_id, Company.name, Company.address, Company.website FROM Company INNER JOIN attends ON Company.company_id = attends.companyID INNER JOIN CareerFair ON CareerFair.cf_id = attends.cfID AND CareerFair.name = \'" + careerfair_name + "\' ")
    careerfair = CareerFair.objects.raw('SELECT cf_id FROM CareerFair ORDER BY year')
    return render(request, 'LonganApp/company.html', context = {
        'companies': company,
        'careerfairs': careerfair,
        'filtered_by': careerfair_name,
        'authenticated': authenticated,
        'superuser': superuser
    })

def temp(email):
    industries = Prefers.objects.raw('SELECT id, industry_name FROM prefers WHERE email =\'' + email + "\'")
    pprint(vars(industries))
    companies = []
    i = 0
    print("test\n")
    for industry in industries:
        a = Company.objects.raw('SELECT Company.company_id, Company.name, Company.website, Company.address, Company.latitude, Company.longitude FROM cinIndustry, Industry, Company, prefers WHERE Company.company_id = cinIndustry.company_id AND Industry.name=\'' + industry.industry_name + '\' AND cinIndustry.industry_id = Industry.industry_id AND Industry.name = prefers.industry_name AND prefers.email = \'' + email + "\'")
        pprint(vars(a))
        print("-----")
        print(i)
        print("-----")
        i += 1
        for b in a:
            print(b.name)
            print("\nWHYYYYYYY\n")
            c = Company.create(b.company_id, b.name, b.address, b.website, b.latitude, b.longitude)
            print(c.name)
            companies.append(c)

    result = []
    if len(companies) != 0:
        print("NOT EQUALS TO ZERO\n")
        count = 0
        favorites = Company.objects.raw('SELECT Company.company_id, Company.name, Company.website, Company.address, Company.latitude, Company.longitude FROM favorites, Company WHERE favorites.email =\'' + email + "\' AND Company.name = favorites.companyName");
        print(i)
        searched = 0

        while count < 5 and searched < len(companies):
            searched += 1
            i = randint(0, len(companies)-1)
            found = False
            for x in result:
                if x.company_id == companies[i].company_id:
                    found = True
                    i = i + 1
                    if i == len(companies):
                        i = 0
                    break

            if found == False:
                for favorite in favorites:
                    print("for each favorite\n")
                    # print("companies:\n")
                    # pprint (vars(companies[i]))
                    # print(companies[i])
                    # print("\n")
                    # print("fav:\n")
                    # pprint (vars(favorite))
                    # print(favorite)
                    # print("\n")
                    if distance(favorite.latitude, favorite.longitude, companies[i].latitude, companies[i].longitude) < 1000:
                        d = Company.create(companies[i].company_id, companies[i].name, companies[i].address, companies[i].website, companies[i].latitude, companies[i].longitude)
                        result.append(d)
                        count += 1
                        break

    return result


def company(request):
    suggestions = ''
    if request.user.is_authenticated:
        authenticated = 'true'
        suggestions = temp(request.user.email)
        if request.user.is_superuser:
            superuser = 'true'
        else:
            superuser = 'false'
    else:
        authenticated = 'false'
        superuser = 'false'
    careerfair = CareerFair.objects.raw('SELECT cf_id FROM CareerFair ORDER BY year')
    company = Company.objects.raw('SELECT company_id FROM Company ORDER BY name')
    return render(request, 'LonganApp/company.html', context = {
        'companies': company,
        'careerfairs': careerfair,
        'authenticated': authenticated,
        'superuser': superuser,
        'suggestions': suggestions
    })

def addCompanyToJson(name, zip):
    with open('LonganApp/media/LonganApp/data.json') as outfile:
        data = json.load(outfile)
    with open('LonganApp/c.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        with open('LonganApp/media/LonganApp/data.json', 'w') as outfile:
            for row in readCSV:
                if row[0] == str(zip):
                    with connection.cursor() as cursor:
                        cursor.execute("UPDATE Company SET longitude = " + row[1] + ", latitude = " + row[2] + " WHERE name = \'" + name + "\';")
                    a_dict = {str(name): [float(row[1]), float(row[2])]}
                    data.update(a_dict)
                    json.dump(data, outfile)

def addCompany(request):
    with connection.cursor() as cursor:
        name = request.POST['name']
        address = request.POST['address']
        website = request.POST['website']
        cursor.execute("INSERT INTO Company(name, address, website, longitude, latitude) VALUES (\'" + name + "\', \'" + address + "\', \'" + website + "\', 0, 0)")
        addCompanyToJson(name, int(address[-5:]))
    return redirect("https://cs411spring2017.pythonanywhere.com/company.html")

def deleteCompanyInJson(name):
    with open('LonganApp/media/LonganApp/test.json', 'r') as outfile:
        data = json.load(outfile)
    data.pop(name, None)
    with open('LonganApp/media/LonganApp/test.json', 'w') as outfile:
        data = json.dump(data, outfile)

def deleteCompany(request):
    with connection.cursor() as cursor:
        companyName = request.POST['companyName']
        cursor.execute("DELETE FROM Company WHERE name = %s", [companyName])
        deleteCompanyInJson(companyName)
    return redirect("https://cs411spring2017.pythonanywhere.com/company.html")

def updateCompany(request):
    with connection.cursor() as cursor:
        name = request.POST['name']
        address = request.POST['address']
        website = request.POST['website']
        oldName = request.POST['oldName']
        cursor.execute("UPDATE Company SET name = \'" + name + "\', address = \'" + address + "\', website = \'" + website + "\' WHERE name = \'" + oldName + "\'")
    return redirect("https://cs411spring2017.pythonanywhere.com/company.html")

def filterByCompany(request):
    company_name = request.POST['company']
    if not company_name:
        return redirect("https://cs411spring2017.pythonanywhere.com/careerfair.html")
    careerfair = CareerFair.objects.raw("SELECT CareerFair.cf_id, CareerFair.name, CareerFair.year, CareerFair.semester, CareerFair.location FROM CareerFair, Company, attends WHERE Company.name = \'" + company_name + "\' AND CareerFair.cf_id = attends.cfID AND Company.company_id = attends.companyID")
    return render(request, 'LonganApp/careerfair.html', context = {
        'companies': Company.objects.raw('SELECT company_id FROM Company ORDER BY name'),
        'careerfairs': careerfair,
        'filtered_by': company_name
    })
