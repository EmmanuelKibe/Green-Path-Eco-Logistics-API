from celery import shared_task
from .services import calculate_distance 

@shared_task
def compute_shipment_metrics_task(shipment_id):
    from .models import Shipment
    try:
        shipment = Shipment.objects.select_related('vehicle').get(id=shipment_id)
        
        # Handle Distance if missing
        if not shipment.distance:
            calculated = calculate_distance(shipment.origin, shipment.destination)
            shipment.distance = calculated if calculated else 0
        
        # 2. Perform Carbon Calculation
        # We convert to float/Decimal safely
        dist = float(shipment.distance)
        wgt = float(shipment.weight)
        factor = float(shipment.vehicle.emission_factor)
        
        shipment.carbon_footprint = dist * wgt * factor
        
        # 3. Save only the calculated fields
        shipment.save(update_fields=['distance', 'carbon_footprint'])
        
        return f"Shipment {shipment_id} processed successfully."
    
    except Shipment.DoesNotExist:
        return f"Shipment {shipment_id} not found."