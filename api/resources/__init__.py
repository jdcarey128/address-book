def _validate_field(data, field, proceed, errors, missing_okay=False):
  if field in data: 
    data[field] = data[field].strip()
    if len(data[field]) == 0:
      proceed = False 
      errors.append(f"required '{field}' parameter is blank")
  if not missing_okay and field not in data:
    proceed = False 
    errors.append(f"required '{field}' parameter is missing")
    data[field] = ''
  if missing_okay and field not in data: 
    return proceed, None, errors

  return proceed, data[field], errors

def _error_400(errors):
  return {
        'success': False, 
        'error': 400,
        'errors': errors
  }, 400
