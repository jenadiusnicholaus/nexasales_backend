import os


def profile_pictureupload_to(instance):
    """
    Generate the upload path for the document in the format:
    doc_type/contain_name/files/<filename>
    """
    # Access doc_type and user_name from the instance
    user_name = instance.username  # Assuming `Entity` has a `user` field
    doctype = "pictures"
    contain_name = "profiles"

    # Construct the path
    return os.path.join(doctype, contain_name, user_name)


def document_upload_to(instance, filename):
    """
    Generate the upload path for the document in the format:
    doc_type/user_name/files/<filename>
    """
    # Access doc_type and user_name from the instance
    doc_type = instance.doc_type
    user_name = instance.user.username  # Assuming `Entity` has a `user` field
    # Construct the path
    return os.path.join(doc_type, user_name, filename)
