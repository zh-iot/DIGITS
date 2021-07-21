(function(window){
    var gt = new Gettext({domain: 'digits'});
    var gettext = function(msgid) { return gt.gettext(msgid); };
    var ngettext = function(msgid, msgid_plural, n) { return gt.ngettext(msgid, msgid_plural, n); };

    window.gettext = gettext
    window.ngettext = ngettext
})(window)