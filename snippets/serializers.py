from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # Add a filed to display a list of related snippets.
    #snippets = serializers.PrimaryKeyRelatedField(many=True)
    # Use a hyperlink to the Snippets endpoint.
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'snippets')


#class SnippetSerializer(serializers.Serializer):
#    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
#    title = serializers.CharField(required=False,
#                                  max_length=100)
#    code = serializers.CharField(widget=widgets.Textarea,
#                                 max_length=100000)
#    linenos = serializers.BooleanField(required=False)
#    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES,
#                                       default='python')
#    style = serializers.ChoiceField(choices=STYLE_CHOICES,
#                                    default='friendly')
#
#    def restore_object(self, attrs, instance=None):
#        """
#        Create or update a new snippet instance, given a dictionary
#        of deserialized field values.
#
#        Note that if we don't define this method, then deserializing
#        data will simply return a dictionary of items.
#        """
#        if instance:
#            # Update existing instance
#            instance.title = attrs.get('title', instance.title)
#            instance.code = attrs.get('code', instance.code)
#            instance.linenos = attrs.get('linenos', instance.linenos)
#            instance.language = attrs.get('language', instance.language)
#            instance.style = attrs.get('style', instance.style)
#            return instance
#
#        # Create new instance
#        return Snippet(**attrs)

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # To make it more user-friendly, let's use the username instead of the default pk. This is
    # optional, obviously.
    owner = serializers.Field(source='owner.username')
    # Add a highlight field to link to the Highlights endpoint.
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        # The `id` field is replaced by the `url` field because this is a
        # `HyperlinkedModelSerializer` sub-class.
        fields = ('id', 'url', 'highlight', 'owner', 'title', 'code', 'linenos', 'language',
                  'style')