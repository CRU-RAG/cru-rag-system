"""
This is a test script to test the embedder
"""

from dotenv import load_dotenv
from services.weaviate.weaviate_service import WeaviateService

load_dotenv(override=True)

weaviate_service = WeaviateService()
weaviate_service.insert_data(
    "53b01234-2d2f-4748-a182-5b30e335021d",
    "Grace",
    """Grace is the unmerited favor of God bestowed upon undeserving humanity.
                             It is a gift that cannot be earned or deserved, but is freely
                             given. Through grace, we are forgiven of our sins, justified
                             before God, and adopted into His family. It is the foundation
                             of the Christian faith, enabling believers to live a life of
                             righteousness and holiness.""",
)
weaviate_service.insert_data(
    "c303282d-f2e6-46ca-a04a-35d3d873712d",
    "Faith",
    """Faith is the substance of
                             things hoped for,the evidence of things not seen.
                             It is the trust and reliance upon God, His promises,
                             and His character. Faith is not merely belief,
                             but a confident assurance in God's ability to fulfill
                             His Word. It is a gift from God that enables us to overcome
                             obstacles, endure trials, and experience the supernatural.""",
)
weaviate_service.insert_data(
    "a91043e5-942d-4d89-b146-09b933d0c11a",
    "Love",
    """Love is the greatest commandment,
                             surpassing all others. It is the essence of God's character
                             and the driving force behind His actions. Love is patient,
                             kind, and selfless. It does not envy, boast, or pride itself.
                             It does not dishonor others, is not self-seeking, is not easily
                             angered, keeps no record of wrongs. Love rejoices with the truth,
                             always protects, always trusts, always hopes, always perseveres.""",
)
weaviate_service.insert_data(
    "6b987654-e321-4f00-9a95-f5d74b46900a",
    "Ethiopia",
    """Ethiopia is a country located in
                             the Horn of Africa. It is bordered by
                             Sudan to the north, South Sudan to the south.""",
)

print(weaviate_service.search("Gambella", max_distance=0.5, match_limit=1))

print(weaviate_service.item_exists("6b987654-e321-4f00-9a95-f5d74b46900a"))

weaviate_service.delete("6b987654-e321-4f00-9a95-f5d74b46900a")

print(weaviate_service.item_exists("6b987654-e321-4f00-9a95-f5d74b46900a"))
