from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class ROLES(models.TextChoices):
    Supervisor = "Supervisor"
    Instructor = "Instructor"
    TA = "TA"

class Semester(models.TextChoices):
    Spring = "Spring"
    Summer = "Summer"
    Winter = "Winter"
    Fall = "Fall"
class Department(models.TextChoices):
    ACTUARIAL_SCIENCE = 'ACTSCI', 'Actuarial Science'
    ADMINISTRATIVE_LEADERSHIP = 'AD_LDSP', 'Administrative Leadership'
    AFRICAN_AFRICAN_DIASPORA_STUDIES = 'AFRIC', 'African & African Diaspora Studies'
    AIR_FORCE_AEROSPACE_STUDIES = 'AFAS', 'Air Force and Aerospace Studies'
    AMERICAN_INDIAN_STUDIES = 'AIS', 'American Indian Studies'
    ANCIENT_MODERN_LANGUAGES_LITERATURES_CULTURES = 'AMLLC', 'Ancient & Modern Languages, Literatures & Cultures'
    ANTHROPOLOGY = 'ANTHRO', 'Anthropology'
    APPLIED_COMPUTING = 'APC', 'Applied Computing'
    ARABIC = 'ARABIC', 'Arabic'
    ARCHITECTURE = 'ARCH', 'Architecture'
    ART_DESIGN = 'ART', 'Art and Design'
    ART_EDUCATION = 'ART_ED', 'Art Education'
    ART_HISTORY = 'ARTHIST', 'Art History'
    ASTRONOMY = 'ASTRON', 'Astronomy'
    ATHLETIC_TRAINING = 'ATRAIN', 'Athletic Training'
    ATMOSPHERIC_SCIENCES = 'ATM_SCI', 'Atmospheric Sciences'
    BIOLOGICAL_SCIENCES = 'BIO_SCI', 'Biological Sciences'
    BIOMEDICAL_ENGINEERING = 'BME', 'Biomedical Engineering'
    BIOMEDICAL_SCIENCES = 'BMS', 'Biomedical Sciences'
    BUSINESS_ADMINISTRATION = 'BUS_ADM', 'Business Administration'
    BUSINESS_MANAGEMENT = 'BUSMGMT', 'Business Management'
    CELTIC_STUDIES = 'CELTIC', 'Celtic Studies'
    CHEMISTRY_BIOCHEMISTRY = 'CHEM', 'Chemistry and Biochemistry'
    CHINESE = 'CHINESE', 'Chinese'
    CIVIL_ENVIRONMENTAL_ENGINEERING = 'CIV_ENG', 'Civil & Environmental Engineering'
    CLASSICS = 'CLASSIC', 'Classics'
    COLLEGE_HEALTH_SCIENCES = 'CHS', 'College of Health Sciences'
    COMMUNICATION = 'COMMUN', 'Communication'
    COMMUNICATION_SCIENCES_DISORDERS = 'COMSDIS', 'Communication Sciences and Disorders'
    COMPARATIVE_LITERATURE = 'COMPLIT', 'Comparative Literature'
    COMPUTER_SCIENCE = 'COMPSCI', 'Computer Science'
    COMPUTER_STUDIES = 'COMPST', 'Computer Studies'
    CONSERVATION_ENVIRONMENTAL_SCIENCES = 'CES', 'Conservation and Environmental Sciences'
    COUNSELING = 'COUNS', 'Counseling'
    CRIMINAL_JUSTICE_CRIMINOLOGY = 'CRM_JST', 'Criminal Justice & Criminology'
    CURRICULUM_INSTRUCTION = 'CURRINS', 'Curriculum and Instruction'
    DANCE = 'DANCE', 'Dance'
    DIAGNOSTIC_IMAGING = 'DMI', 'Diagnostic Imaging'
    DIGITAL_ARTS_CULTURE = 'DAC', 'Digital Arts and Culture'
    ECONOMICS = 'ECON', 'Economics'
    EDUCATION_INTERDEPARTMENTAL = 'EDUC', 'Education-Interdepartmental'
    EDUCATIONAL_POLICY_COMMUNITY_STUDIES = 'ED_POL', 'Educational Policy and Community Studies'
    EDUCATIONAL_PSYCHOLOGY = 'ED_PSY', 'Educational Psychology'
    ELECTRICAL_ENGINEERING = 'ELECENG', 'Electrical Engineering'
    ENGINEERING_APPLIED_SCIENCE = 'EAS', 'Engineering and Applied Science'
    ENGLISH = 'ENGLISH', 'English'
    ENGLISH_ACADEMIC_PURPOSES = 'EAP', 'English for Academic Purposes'
    ETHNIC_STUDIES_COMPARATIVE = 'ETHNIC', 'Ethnic Studies, Comparative'
    EXCEPTIONAL_EDUCATION = 'EXCEDUC', 'Exceptional Education'
    FILM_STUDIES = 'FILMSTD', 'Film Studies'
    FILM_VIDEO_ANIMATION_NEW_GENRES = 'FILM', 'Film, Video, Animation and New Genres'
    FOOD_BEVERAGE_STUDIES = 'FOODBEV', 'Food & Beverage Studies'
    FRENCH = 'FRENCH', 'French'
    FRESHWATER_SCIENCES = 'FRSHWTR', 'Freshwater Sciences'
    GEOGRAPHY = 'GEOG', 'Geography'
    GEOSCIENCES = 'GEO_SCI', 'Geosciences'
    GERMAN = 'GERMAN', 'German'
    GLOBAL_STUDIES = 'GLOBAL', 'Global Studies'
    GRADUATE_STUDIES = 'GRAD', 'Graduate Studies'
    GREEK = 'GREEK', 'Greek'
    HEALTH_CARE_ADMINISTRATION = 'HCA', 'Health Care Administration'
    HEALTH_CARE_INFORMATICS = 'HI', 'Health Care Informatics'
    HEALTH_SCIENCES = 'HS', 'Health Sciences'
    HEBREW = 'HEBREW', 'Hebrew'
    HISTORY = 'HIST', 'History'
    HMONG_STUDIES = 'HMONG', 'Hmong Studies'
    HONORS_COLLEGE = 'HONORS', 'Honors College'
    INDUSTRIAL_LABOR_RELATIONS = 'IND_REL', 'Industrial and Labor Relations'
    INDUSTRIAL_MANUFACTURING_ENGINEERING = 'IND_ENG', 'Industrial and Manufacturing Engineering'
    INFORMATION_STUDIES = 'INFOST', 'Information Studies'
    INTERNATIONAL_STUDIES = 'INTLST', 'International Studies'
    ITALIAN = 'ITALIAN', 'Italian'

class Number(models.TextChoices):
    SECTION_001 = '001'
    SECTION_002 = '002'
    SECTION_003 = '003'


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, phone,
                    is_instructor, is_assistant, is_admin, is_superuser):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_instructor=is_instructor,
            is_assistant=is_assistant,
            is_admin=is_admin,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name,
                         phone, is_instructor, is_assistant, is_admin):
        user = self.create_user(email, password, first_name, last_name, phone,
                                is_instructor, is_assistant, is_admin, is_superuser=True)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # password = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    role = models.CharField(max_length=20, choices=ROLES.choices, default="TA")
    is_instructor = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone',
                       'is_instructor', 'is_assistant', 'is_admin']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_staff(self):
        return self.is_admin


class Course(models.Model):
    department = models.CharField(max_length=20, choices=Department.choices, default="COMPSCI")
    number =  models.IntegerField()
    name = models.CharField(max_length=30)
    semester = models.CharField(max_length=20, choices=Semester.choices, default="Fall")

    def __str__(self):
        return self.name


class Lab(models.Model):
    assistant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_assistant': True}
    )
    lab_name = models.CharField(max_length=20, choices=Number.choices, default="001")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length=13, default="Mo We")

    def __str__(self):
        return self.lab_name


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_instructor': True}
    )
    section_name = models.CharField(max_length=20, choices=Number.choices, default="001")
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length=13, default="Tu Th")

    def __str__(self):
        return self.section_name
