from django.db import models

class ScanReport(models.Model):
    FILE_TYPES = [
        ('document', 'Document'),
        ('photo', 'Photo / Image'),
        ('video', 'Video'),
    ]
    VERDICT_CHOICES = [
        ('fake', 'Fake'),
        ('real', 'Real'),
        ('suspicious', 'Suspicious'),
    ]

    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    file_size = models.PositiveIntegerField(help_text="Size in KB")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES)
    fake_score = models.IntegerField(help_text="0-100, higher = more likely fake")
    issues_found = models.PositiveIntegerField(default=0)
    warnings_found = models.PositiveIntegerField(default=0)

    # Detailed check results stored as JSON text
    checks_json = models.TextField(default='[]')
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.file_name} — {self.verdict} ({self.fake_score}%)"

    class Meta:
        ordering = ['-uploaded_at']
