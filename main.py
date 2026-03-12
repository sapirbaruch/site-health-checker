from checker import check_site


def main():
    # URL to check
    url = "https://example.com"

    result = check_site(url)
    print("Report:")

    # Print report content in a readable format
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    # Run main function when the script is executed directly
    main()