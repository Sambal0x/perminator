import xml.etree.ElementTree as ET
import sys
import argparse

# Function to print the Perminator ASCII art
def print_perminator_ascii():
    print("""
························································
: ____                     _             _             :
:|  _ \ ___ _ __ _ __ ___ (_)_ __   __ _| |_ ___  _ __ :
:| |_) / _ \ '__| '_ ` _ \| | '_ \ / _` | __/ _ \| '__|:
:|  __/  __/ |  | | | | | | | | | | (_| | || (_) | |   :
:|_|   \___|_|  |_| |_| |_|_|_| |_|\__,_|\__\___/|_|   :
························································
    """)

# Function to check if permission is declared in the <permission> section
def check_permission_in_permission_tag(permission, permissions):
    for perm in permissions:
        if perm.get('{http://schemas.android.com/apk/res/android}name') == permission:
            return True
    return False

# Function to parse AndroidManifest.xml and check permissions
def check_permissions(manifest_path, skip_common_permissions):
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()

        # Define the namespace to handle elements correctly
        namespace = {'android': 'http://schemas.android.com/apk/res/android'}

        # Find all permission declarations (for general permission definitions)
        permissions = root.findall(".//permission")
        declared_permissions_in_permission_tag = [perm.get('{http://schemas.android.com/apk/res/android}name') for perm in permissions]
        
        # Print out all declared permissions for debugging purposes
        print(f"\nDeclared permissions in <permission>:\n{declared_permissions_in_permission_tag}\n")

        # Check each component for android:permission
        issues_found = False
        for component in ['activity', 'service', 'receiver', 'provider']:
            for elem in root.findall(f".//{component}"):
                permission = elem.get('{http://schemas.android.com/apk/res/android}permission')
                if permission:
                    print(f"Detected permission '{permission}' in <{component}>")

                    # Skip checking if the permission starts with "android.permission" or "com.google.android" (if flag is set)
                    if skip_common_permissions and (permission.startswith("android.permission") or permission.startswith("com.google.android")):
                        print(f"\033[92mSkipping common permission '{permission}' in <{component}>.\033[0m")
                        continue

                    # Ensure the permission is listed in <permission> tag
                    if permission not in declared_permissions_in_permission_tag:
                        print(f"\033[91mIssue: Permission '{permission}' declared in <{component}> is not listed in <permission>\033[0m")
                        issues_found = True
                    else:
                        print(f"\033[92mAll good: Permission '{permission}' declared in <{component}> is listed in <permission>\033[0m")

        # If no issues were found
        if not issues_found:
            print("\033[92mNo issues found. All permissions are correctly declared.\033[0m")

    except ET.ParseError as e:
        print(f"\033[91mError parsing AndroidManifest.xml: {e}\033[0m")
    except FileNotFoundError:
        print("\033[91mThe AndroidManifest.xml file was not found.\033[0m")

# Main function to handle command-line arguments
def main():
    print_perminator_ascii()  # Print the Perminator ASCII art when the script starts
    
    parser = argparse.ArgumentParser(description="Check AndroidManifest.xml for correct permission declarations.")
    parser.add_argument("manifest_path", help="Path to the AndroidManifest.xml file.")
    parser.add_argument("--skip-common-permissions", action="store_true", help="Skip common system and Google permissions (those starting with 'android.permission' or 'com.google.android').")
    args = parser.parse_args()

    # Run the permission check with the flag if set
    check_permissions(args.manifest_path, args.skip_common_permissions)

if __name__ == '__main__':
    main()

