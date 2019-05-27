jQuery(document).ready(function(){
    if (django.jQuery('form[name="profile_form"]').length || django.jQuery('#changelist').length) {
        django.jQuery(".field-name").show();
        django.jQuery(".field-email").show();
        django.jQuery(".field-latitude").show();
        django.jQuery(".field-longitude").show();
        django.jQuery(".field-birth_date").show();
        django.jQuery(".field-photo").show();
    }else
    {
        django.jQuery(".field-name").hide();
        django.jQuery(".field-email").hide();
        django.jQuery(".field-latitude").hide();
        django.jQuery(".field-longitude").hide();
        django.jQuery(".field-birth_date").hide();
        django.jQuery(".field-photo").hide();
    }

    django.jQuery('input[type="checkbox"]').click(function()
   {
      if( this.checked)
      {
        django.jQuery(".field-name").show();
        django.jQuery(".field-email").show();
        django.jQuery(".field-latitude").show();
        django.jQuery(".field-longitude").show();
        django.jQuery(".field-birth_date").show();
        django.jQuery(".field-photo").show();
      }
      else
      {
        django.jQuery(".field-name").hide();
        django.jQuery(".field-email").hide();
        django.jQuery(".field-latitude").hide();
        django.jQuery(".field-longitude").hide();
        django.jQuery(".field-birth_date").hide();
        django.jQuery(".field-photo").hide();
      }
   }
   );
});


