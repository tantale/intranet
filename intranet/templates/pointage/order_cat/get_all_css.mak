%if display == 'html':
<h2>Feuille de styles CSS des catégories de commandes</h2>
<pre>
%for order_cat in order_cat_list:
.${order_cat.cat_name} {${order_cat.css_def}}
%endfor
</pre>
%else:
%for order_cat in order_cat_list:
.${order_cat.cat_name} {${order_cat.css_def}}
%endfor
%endif