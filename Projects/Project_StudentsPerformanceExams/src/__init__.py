# __init__.py is a special file Python looks for when treating a folder as a package.

# Smart __init__.py used for importing easily from the package.

try:
	from .data_loader import load_csv, load_excel, load_list, load_dict
except ImportError as e:
	raise ImportError("The 'dataloader' module could not be found. Ensure it exists in the same directory as '__init__.py'.") from e

__all__ = [load_csv, load_excel_ sheet, load_list, load_dict, 
           missing_values, normalize_string, drop_explicit_duplicates,
           replace_string_numeric_values_numeric, replace_missing_numeric_values_zero,
           replace_missing_numeric_values_mean, replace_missing_numeric_values_median, 
           replace_missing_string_values, replace_string_datetime_values_datetime, 
           detect_implicit_duplicates,]