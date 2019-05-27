django.jQuery(document).ready(function(){

    if (django.jQuery('form[name="profile_form"]').length || django.jQuery('#changelist').length) {
        django.jQuery(".field-phone_number").show();
        django.jQuery(".field-phone_country").hide();
    }else
    {
       django.jQuery(".field-phone_number").hide();
       django.jQuery(".field-phone_country").show();
    }

    django.jQuery('input[type="checkbox"]').click(function()
   {
      if( this.checked)
      {
         django.jQuery(".field-phone_number").show();
         django.jQuery(".field-phone_country").hide();
      }
      else
      {
         django.jQuery(".field-phone_number").hide();
         django.jQuery(".field-phone_country").show();
      }
   }
   );
});


