from rest_framework import serializers
from .models import BeekeeperSession, RiskProfile, Claim


class ClaimSerializer(serializers.ModelSerializer):
    """
    Serializer for insurance claims.
    """
    class Meta:
        model = Claim
        fields = ['id', 'profile', 'image_url', 'confidence', 'status', 'created_at']
        read_only_fields = ['created_at']

    def validate_confidence(self, value):
        """
        Validate that confidence score is between 0 and 1.
        """
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Confidence score must be between 0 and 1")
        return value


class RiskProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for beekeeper risk profiles.
    Includes nested claims data.
    """
    claims = ClaimSerializer(many=True, read_only=True)

    class Meta:
        model = RiskProfile
        fields = ['id', 'session', 'score', 'level', 'premium', 'cover_amount', 
                 'generated_at', 'claims']
        read_only_fields = ['generated_at']

    def validate_score(self, value):
        """
        Validate that risk score is between 0 and 100.
        """
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Risk score must be between 0 and 100")
        return value


class BeekeeperSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for beekeeper USSD sessions.
    Includes nested risk profiles data.
    """
    risk_profiles = RiskProfileSerializer(many=True, read_only=True)

    class Meta:
        model = BeekeeperSession
        fields = ['id', 'session_id', 'phone_number', 'inputs', 'created_at', 
                 'risk_profiles']
        read_only_fields = ['created_at']