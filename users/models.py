from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from PIL import Image
from django.urls import reverse

### Documentation: ###
# See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
'''
    If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you.
    This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises.
    Configure users.User to be the model used for the auth application by adding AUTH_USER_MODEL to settings.py:
    AUTH_USER_MODEL='users.User'
'''
# THIS NEEDS TO BE DONE PRIOR TO THE FIRST DB MIGRATION OR YOUR APP WILL FAIL


### for reference, follow-along: https://www.youtube.com/watch?v=mndLkCEiflg

class CustomUserManager(UserManager):
    '''
        Our own UserManager that we will use when using the manage.py file
    '''
    def _create_user(self, staff_id, password, **extra_fields):
        if not staff_id:
            '''check if the user provided a valid email address'''
            raise ValueError("Please provide a valid Staff ID.")

        # email = self.normalize_email(email)
        user = self.model(staff_id=staff_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    '''function used in cmd to create a regular user'''
    def create_user(self, staff_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(str(staff_id), password, **extra_fields) #string-ify staff_id to avoid errors on forms when editing it in the future

    '''function used in cmd to create a super user'''
    def create_superuser(self, staff_id=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # just double-checking the superuser creation meets the required priviledges
        # __( I asked chatGPT what these two if lines are for. XD )__
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(staff_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''
        the default (custom) User model the app will use 
    '''
    objects = CustomUserManager() # settign CustomUserManager() instead of default UserManager()

    staff_id = models.PositiveIntegerField(unique=True) # change max_length if needed, add min_length/value
    email = models.EmailField(blank=True, default="") # add unique & null field options in production!
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    

    USERNAME_FIELD = "staff_id" # usually this is "email" but because of what we set on the CustomUserManager(), main identifier is staff_id
    REQUIRED_FIELDS = [] # ["email", "username", "first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = 'Users'
        
    def __str__(self):
        return str(self.staff_id)

    def get_short_name(self):
        return str(self.staff_id)


# class EmployeeClassification(models.Model):
#     '''
#         What are the user types of the app?
#         Default will be Agent but admin can set it to whatever is needed.
#         Just add instances of this class and they will be fetched as options for the "classification" attr of the Profile class.
#     '''
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name          = models.CharField(max_length=50, blank=True)
    middle_name         = models.CharField(max_length=50, blank=True)
    last_name           = models.CharField(max_length=50, blank=True)
    ext_name            = models.CharField(max_length=3, blank=True)


    class Classification(models.TextChoices):
        AGENT = "AGENT", "Agent"
        TL = "TL", "Team Leader"
        OM = "OM", "Operations Mgr"

    ### determining user classification
    classification = models.CharField(verbose_name=("User Classification: "), blank=True, max_length=80, choices=Classification.choices, default=Classification.AGENT)


    Dept01 = "Department 01"
    Dept02 = "Department 02"
    Dept03 = "Department 03"
    dept_choices = [
        (Dept01, "Dept01"),
        (Dept02, "Dept02"),
        (Dept03, "Dept03")
    ]

    ### what department they would be in
    ### Note: Choices here were hard-coded (see above) for it's not often that new depts are created
    department          = models.CharField(
        max_length=20,
        choices=dept_choices,
        default=Dept01, verbose_name="Department: "
    )
    
    def dp_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/DP/<username>/<filename> ---check settings.py. MEDIA_ROOT=media for the exact folder/location
        return 'users/{}/DP/{}'.format(instance.user.staff_id, filename)
    image = models.ImageField(default='defaults/default_user_dp.png', blank=True, upload_to=dp_directory_path, verbose_name="Display Photo: ", help_text='Help us recognize you better. ;)')

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.ext_name} {self.middle_name}".strip()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):        # for resizing/downsizing images
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)   # open the image of the current instance
        if img.height > 600 or img.width > 600: # for sizing-down the images to conserve memory in the server
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)