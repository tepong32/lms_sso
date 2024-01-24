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


class Manager(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class WorkGroup(models.Model):
    select = "---select one---"
    SFST    = "Secured Financial Support Team"
    UFST    = "UnSecured Financial Support Team"
    AUH     = "Australia Collections"
    AU      = "Australia"
    PH      = "Philippines"
    SG      = "Singapore"
    MSS     = "Marks & Spencer"
    HRS     = "HSBC Repayment Services"
    US      = "US"
    CANADA  = "CANADA"
    OTPA    = "Outcome Testing Policy Adherence"

    choices = [
        (select, "---select one---"),
        (SFST, "Secured Financial Support Team"),
        (UFST, "UnSecured Financial Support Team"), 
        (AUH, "Australia Collections"),
        (AU, "Australia"),
        (PH, "Philippines"),
        (SG, "Singapore"),
        (MSS, "Marks & Spencer"),
        (HRS, "HSBC Repayment Services"),
        (US, "United States"),
        (CANADA, "Canada"),
        (OTPA, "Outcome Testing Policy Adherence")
        ]

    name = models.CharField(blank=True, null=False, max_length=80, choices=choices, default=select, verbose_name="Workgroup: ")
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=False)
    ### setting max_allowable leaves per "cluster"/OM
    allowed_leaves_per_day = models.PositiveIntegerField(null=True, blank=True, default=20,
        help_text='''
            This will help with auto-approve leave requests.
            Computation will be: allowed leaves - approved leaves for the day. If there are still available allowed_leaves_per_day instances, the leave requests will be auto-approved.
            If there are none, the leave status will just be set to default: "Pending".
        ''')
    
    class Meta:
        verbose_name_plural = "Workgroups"

    def __str__(self):
        return f"{self.name} - {self.manager}".strip()


class User(AbstractBaseUser, PermissionsMixin):
    '''
        Custom User model the app will use 
    '''
    ### key identifier attributes
    staff_id = models.PositiveIntegerField(unique=True) # change max_length if needed, add min_length/value
    email = models.EmailField(unique=True) # add unique & null field options in production!

    ### misc default User attributes
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  ############################### <-- disabled user account after registration, SET TO TRUE FOR THE FIRST TIME!
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    ### setting user type for permissions-related queries
    is_advisor          = models.BooleanField(default=True) ### <-- default is all users that register are advisors
    is_team_leader      = models.BooleanField(default=False)
    is_operations_manager  = models.BooleanField(default=False)

    ### personal info <-- this should match company records as much as possible
    first_name          = models.CharField(max_length=50)
    middle_name         = models.CharField(max_length=50, blank=True)
    last_name           = models.CharField(max_length=50)
    ext_name            = models.CharField(max_length=3, blank=True, null=True, verbose_name="Extension")
    workgroup           = models.ForeignKey(WorkGroup, on_delete=models.SET_NULL, null=True, blank=False)
    
    objects = CustomUserManager() # set the CustomUserManager() above instead of default UserManager() from django.contrib.auth

    USERNAME_FIELD = "staff_id" # the key identifier of accounts. This was also set on the CustomUserManager() class code
    REQUIRED_FIELDS = [] # ["email", "username", "first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = 'Users'
        
    def __str__(self):
        if {self.last_name} and {self.first_name}:
            return f"{self.last_name}, {self.first_name}".strip().title()
        else:
            return str(self.staff_id)

    def get_short_name(self):
        return str(self.staff_id)

    def dp_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/DP/<username>/<filename> ---check settings.py. MEDIA_ROOT=media for the exact folder/location
        return 'users/{}/DP/{}'.format(instance.user.staff_id, filename)
    image = models.ImageField(default='defaults/default_user_dp.png', blank=True, upload_to=dp_directory_path, verbose_name="Photo")

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):        # for automatically down-sizing images
        super(User, self).save(*args, **kwargs)

        img = Image.open(self.image.path)   # open the image of the current instance
        if img.height > 600 or img.width > 600: # for sizing-down the images to conserve memory in the server
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)