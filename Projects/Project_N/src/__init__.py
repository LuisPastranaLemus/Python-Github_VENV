# __init__.py is a special file Python looks for when treating a folder as a package.

# Smart __init__.py used for importing easily from the package.

try:
	from .dataloader import load_csv, load_excel, load_list, load_dict
except ImportError as e:
	raise ImportError("The 'dataloader' module could not be found. Ensure it exists in the same directory as '__init__.py'.") from e



__all__ = [load_csv, load_excel_ sheet, load_list, load_dict]