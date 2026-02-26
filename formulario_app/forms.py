from django import forms

from .models import ReclamoEntidad, Ris


class ReclamoForm(forms.ModelForm):

    ris = forms.ModelChoiceField(
    queryset=Ris.objects.filter(estado__in=[1, 2]),
    to_field_name="id",
    empty_label="Seleccione una sede",
    label="Sede",
    widget=forms.Select(attrs={'class': 'form-control'})
)

    entidad2 = forms.IntegerField(   # 👈 acepta cualquier número
        label="Unidad orgánica",
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_entidad'}),
     )

    class Meta:
        model = ReclamoEntidad
        
        # SOLO LOS CAMPOS QUE APARECERÁN EN EL FORMULARIO
        fields = [
            'nombres',
            'cargo',
            'celular',
            'tipo_incidencia',
            'anydesk',
            'detalle_solicitud',
            'ris',
             'entidad2',
            'piso',
            'correo_usuario'
        ]

        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_incidencia': forms.Select(attrs={'class': 'form-select'}),
            'anydesk': forms.TextInput(attrs={'class': 'form-control'}),
            'detalle_solicitud': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ris': forms.Select(attrs={'class': 'form-control'}),  # <---- AQUI
             'entidad2': forms.NumberInput(attrs={'class': 'form-control'}),  # <--- corregido
            'piso': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo_usuario': forms.EmailInput(attrs={'class': 'form-control'}),
        }


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ris_id = self.cleaned_data['ris'].id  # <-- Guardar el ID en el modelo
        if commit:
            instance.save()
        return instance