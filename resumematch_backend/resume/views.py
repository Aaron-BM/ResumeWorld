from django.shortcuts import render, get_object_or_404
import re
from .models import Resume
from .serializers import ResumeSerializer, UserRegistrationSerializer
from .utils import pdf_parser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny


job_listings = [
    {
        "title": "Python Developer at TechCorp",
        "skills_required": ["python", "django"]
    },
    {
        "title": "Frontend Developer at PixelSoft",
        "skills_required": ["html", "css", "javascript"]
    },
    {
        "title": "Data Analyst at DataWiz",
        "skills_required": ["python", "postgresql"]
    },
    {
        "title": "Backend Engineer at Backendify",
        "skills_required": ["django", "postgresql"]
    },
]


# Create your views here.
def extract_email(text):
  # text = 'Nothing heren'
  pat = r"[a-zA-Z0-9._]+@[a-z]+(\.[a-z]+)+"
  res = re.search(pat, text)
  return res.group() if res else 'None'
  # print(res.group() if res else 'None')


class ResumeViewSet(viewsets.ModelViewSet):
  serializer_class = ResumeSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Resume.objects.filter(user=self.request.user)


  def create(self, request):
    # 1. Deserialize and validate
    serializer = self.get_serializer(data = request.data)
    ...

    # 2. Save to DB and get object
    if serializer.is_valid():
      resume = serializer.save(user=request.user)
      path = resume.upload.path
      # 3. Extract text and email
      text = pdf_parser.extract_text_from_pdf(path)
      skills = pdf_parser.extract_skill_from_parsed_text(text)
      print("SKILLS",skills)
      mail = extract_email(text)
      ...

      # 4. Update and save again
      resume.parsed_text = text
      resume.email = mail
      resume.skills = skills
      resume.save()
      ...

      # 5. Return response
      return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  @action(detail=True, methods=['get'])
  def match_jobs(self, request, pk = None):
    resume = get_object_or_404(Resume,pk=pk)
    matched_jobs = []
    for job in job_listings:
      matched_skills = [skill for skill in resume.skills if skill.lower() in map(str.lower, job['skills_required'])]
      needed_skills = set(map(str.lower,job["skills_required"])) - set(matched_skills)
      matched_count = len(matched_skills)
      if matched_count > 0:
          per = matched_count/len(job['skills_required']) * 100
          matched_jobs.append({
            'Title': job['title'],
            'match_percentage': round(per,2),
            'needed_skills': needed_skills
          })
    matched_jobs.sort(key= lambda x: x['match_percentage'], reverse=True)

    return Response({"matched_jobs": matched_jobs}, status=status.HTTP_200_OK)
  

class RegisterUserView(APIView):
  permission_classes = [AllowAny]
  
  def post(self, request):
    serializers = UserRegistrationSerializer(data = request.data)
    if serializers.is_valid():
      serializers.save()
      return Response({"message": "User created successfully"},status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



