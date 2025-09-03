export const formatCurrency = new Intl.NumberFormat('en-CA', {
    style: 'currency',
    currency: 'CAD',
    maximumFractionDigits: 0,
});

export function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
  
    const features = formData.getAll("Features");
    const data = {
      ...Object.fromEntries(formData.entries()),
      Features: features, // overwrite with all features
    };
    
    fetch('/api/build', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'application/json' },
    });
}
