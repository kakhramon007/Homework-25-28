from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import User_detail, Video_model, Comment
from phonenumber_field.formfields import PhoneNumberField


class UserRegisterForm(forms.ModelForm):
    phone_number = PhoneNumberField(max_length=13, label='Phone Number', region='UZ')
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8, label='Create Password:')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:')

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists!')

        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User_detail.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number already exists!')

        # Ensure the number starts with "+998"
        if phone_number.country_code != 998:  # Country code for Uzbekistan
            raise forms.ValidationError('Invalid country code! Phone number must belong to Uzbekistan.')

        # Check valid prefixes
        valid_prefixes = (
            '90', '91', '93', '94', '95', '97', '98', '99', '88',
            '70', '71', '75', '76', '78', '79', '20', '33', '50',
            '55', '61', '62', '65', '66', '67', '69'
        )

        # Extract the national number (local part) and validate the prefix
        local_number = str(phone_number.national_number)  # Convert to string
        if not any(local_number.startswith(prefix) for prefix in valid_prefixes):
            raise forms.ValidationError('Invalid prefix for Uzbekistan phone number!')

        # Ensure the rest of the number contains only digits
        if not local_number.isdigit():
            raise forms.ValidationError('The phone number must contain only digits after the prefix.')

        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User_detail.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match!')

        validate_password(password)

        return password


class VideoRegisterForm(forms.ModelForm):
    class Meta:
        model = Video_model
        fields = ['video_title', 'video_content']
        widgets = {
            'video_title': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter video title'}),
        }

    def clean_video_content(self):
        video = self.cleaned_data.get('video_content')
        if video:
            if not video.name.endsiwith(('.mp4', '.mov', '.avi')):
                raise forms.ValidationError('Invalid video format. Only MP4, MOV and AVI are supported.')
        return video


class CommentRegisterForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3})
        }







