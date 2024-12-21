from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Course(models.Model):
    """Course model for different types of English courses."""
    COURSE_CHOICES = [
        ('GE', 'General English'),
        ('EE', 'Extreme English'),
    ]
    
    name = models.CharField(max_length=2, choices=COURSE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()

class Class(models.Model):
    """Class model representing a specific class instance."""
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['start_date', 'name']

    def __str__(self):
        return f"{self.course} - {self.name}"

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")

class Student(models.Model):
    """Student model containing basic student information."""
    student_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True)
    current_class = models.ForeignKey(Class, on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateField()
    participation = models.TextField(blank=True)
    teacher_comments = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    class Meta:
        ordering = ['student_id']

class Assessment(models.Model):
    """Base model for all types of assessments."""

    STATUS_CHOICES = [
        ('COM', 'Completed'),
        ('NA', 'Not Given'),
        ('HOL', 'Holiday'),
        ('ABS', 'Absent'),
        ('DNS', 'Did Not Submit')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    week = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='COM'
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_submissions'
    )

    class Meta:
        abstract = True
        ordering = ['student', 'week', 'skill']

class NumericAssessment(Assessment):
    """Model for assessments with numeric scores (Grammar, Vocabulary, Listening, Reading)."""
    SKILL_CHOICES = [
        ('G', 'Grammar'),
        ('V', 'Vocabulary'),
        ('L', 'Listening'),
        ('R', 'Reading'),
    ]
    
    skill = models.CharField(
        max_length=1, 
        choices=SKILL_CHOICES,
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    total_questions = models.IntegerField(validators=[MinValueValidator(1)])
    correct_answers = models.IntegerField(validators=[MinValueValidator(0)])
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'skill', 'week']
        indexes = [
            models.Index(fields=['student', 'skill', 'week']),
            models.Index(fields=['skill', 'week']),
        ]

    def clean(self):
        if self.status == 'COM':
            if self.correct_answers > self.total_questions:
                raise ValidationError("Cannot have more correct answers than total questions")
            if self.score is None:
                self.score = (self.correct_answers / self.total_questions) * 100
        elif self.status != 'COM':
            self.score = None
            self.correct_answers = 0

    def __str__(self):
        return f"{self.student} - {self.get_skill_display()} Week {self.week}"

class GradedAssessment(Assessment):
    """Model for assessments with letter grades (Writing, Speaking, Pronunciation)."""
    SKILL_CHOICES = [
        ('W', 'Writing'),
        ('S', 'Speaking'),
        ('P', 'Pronunciation'),
    ]

    GRADE_CHOICES = [
        ('A', 'A - Excellent'),
        ('B', 'B - Good'),
        ('C', 'C - Developing'),
        ('D', 'D - Needs Improvement'),
        ('E', 'E - Unsatisfactory')
    ]

    skill = models.CharField(
        max_length=1, 
        choices=SKILL_CHOICES, 
    )
    grade = models.CharField(
        max_length=1,
        choices=GRADE_CHOICES,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ['student', 'skill', 'week']

    def clean(self):
        if self.status == 'COM' and not self.grade:
            raise ValidationError("Grade is required for completed assessments")
        elif self.status != 'COM':
            self.grade = None

    def __str__(self):
        return f"{self.student} - {self.get_skill_display()} Week {self.week}"