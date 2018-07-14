java_pattern = r'%JAVA_VERSION%'
java_versions = [8, 9, 10]


def read_dockerfile():
    with open("./Dockerfile", 'r') as f:
        return f.read()


def main():
    global java_pattern
    global java_versions

    dockerfile = read_dockerfile()

    for version in java_versions:
        modified = dockerfile.replace(java_pattern, str(version))
        with open("./Dockerfile.{}".format(version), 'w') as f:
            f.write(modified)


if __name__ == "__main__":
    main()
