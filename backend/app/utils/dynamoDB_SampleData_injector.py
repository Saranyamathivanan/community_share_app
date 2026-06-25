import boto3
TABLE_NAME='CommunityKnowledge'
def main():
    # 1 - Create Client
    ddb = boto3.resource('dynamodb')
    # ddb = boto3.resource('dynamodb',
    #                     endpoint_url='http://localhost:8000',
    #                     region_name='us-east-1',
    #                     aws_access_key_id='dummy',
    #                     aws_secret_access_key='dummy')
    # 2 - Create the Table
    # table = ddb.create_table(
    #     TableName=TABLE_NAME,
    #     KeySchema=[
    #         {"AttributeName": "UserID", "KeyType": "HASH"},   # Partition key
    #         {"AttributeName": "ContributionID", "KeyType": "RANGE"}  # Sort key
    #     ],
    #     AttributeDefinitions=[
    #         {"AttributeName": "UserID", "AttributeType": "S"},
    #         {"AttributeName": "ContributionID", "AttributeType": "S"},
    #         {"AttributeName": "Country", "AttributeType": "S"},
    #         {"AttributeName": "City", "AttributeType": "S"}
    #     ],
    #     GlobalSecondaryIndexes=[
    #         {
    #             "IndexName": "CountryIndex",
    #             "KeySchema": [
    #                 {"AttributeName": "Country", "KeyType": "HASH"}
    #             ],
    #             "Projection": {"ProjectionType": "ALL"},
    #             "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    #         },
    #         {
    #             "IndexName": "CountryCityIndex",
    #             "KeySchema": [
    #                 {"AttributeName": "Country", "KeyType": "HASH"},
    #                 {"AttributeName": "City", "KeyType": "RANGE"}
    #             ],
    #             "Projection": {"ProjectionType": "ALL"},
    #             "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    #         }
    #     ],
    #     ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
    # )
    # print('Successfully created Table')

    client = boto3.client('dynamodb')
    
    # client = boto3.client('dynamodb',
    #                     endpoint_url='http://localhost:8000',
    #                     region_name='us-east-1',
    #                     aws_access_key_id='dummy',
    #                     aws_secret_access_key='dummy')
    existing_tables = client.list_tables()["TableNames"] 
    print("Existing tables:", existing_tables)
    for item in existing_tables:
        print("Existing tables:",item)
    
    table = ddb.Table(TABLE_NAME)

    # input = {'UserID': '9a112', 'Country': 'OK', 'ContributionID': " 101", 'City': 'New York'}

    input=[
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab8",
        "Country": "New Zealand",
        "City": "Wellington",
        "GeoLocation": "-41.290117721625926, 174.78202502698508",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/te_papa_tongarewa.jpg",
        "Description": "The Museum of New Zealand Te Papa Tongarewa",
        "DetailedDescription": "The Te Papa Museum in Wellington is perfect for those on more of a budget, that still want to learn more about the Māori people. Free to enter, this modern and extensive museum houses more than half a million artefacts that provide a glimpse into Māori history, including a to-scale model of a wharenui or meeting house, replicas of the canoes the Māori first arrived in and a huge collection of authentic artwork. Join a guided tour for the afternoon to get the most out of this remarkable museum.",
        "Category": "Art",
        "KnowledgeType": "Traditonal"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab9",
        "Country": "New Zealand",
        "City": "Coromandel",
        "GeoLocation": "-36.827518, 175.789246",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/cathedral_cove.jpg",
        "Description": "Cathedral Cove",
        "DetailedDescription": "Cathedral Cove is a famous coastal bay known for its dramatic natural limestone arch and white-sand beach. The cove lies within the Te Whanganui-o-Hei / Whanganui A Hei Marine Reserve and is a popular spot for swimming, kayaking and boat tours. It also has cultural significance in Māori tradition (Ngāti Hei) and has appeared in films and music videos, which adds to its fame. Because of visitor pressure and occasional land instability, parts of the walking track and viewing access are managed by the Department of Conservation for safety.",
        "Category": "Place",
        "KnowledgeType": "Traditonal"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab10",
        "Country": "New Zealand",
        "City": "Waitomo",
        "GeoLocation": "-38.260651, 175.103333",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/waitomo_glowworm_cave.jpg",
        "Description": "Waitomo Glowworm Caves",
        "DetailedDescription": "The Waitomo Glowworm Caves are a limestone cave system renowned for the bioluminescent larvae of Arachnocampa luminosa, whose tiny blue-green lights create a \"starry sky\" along the cave ceilings. Most visitors experience the glowworm grotto on a quiet, guided boat ride through the main chamber where lighting is kept minimal to protect the glowworms. The caves are a long-standing tourist attraction and are actively managed with conservation measures and monitoring to protect the fragile cave ecosystem. Waitomo also connects to a broader network of caves in the area (including Ruakuri and Aranui) with varied formations and visitor experiences.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab11",
        "Country": "New Zealand",
        "City": "Wellington",
        "GeoLocation": "–41.2829, 174.7660",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/Wellington_Botanic_Garden.png",
        "Description": "Wellington Botanic Garden",
        "DetailedDescription": "Wellington Botanic Garden is a historic and nationally significant 25-hectare garden, established in 1868. It offers a mix of native forest remnants, curated international plant collections, a vibrant rose garden, Begonia House, fernery, scenic walking trails, sculptures, and a duck pond—all overlooking the city and harbour. The site was originally significant to Te Ātiawa (Pipitea Pā) for its use in food, medicine, fibre, and other resources, and it continues to serve as a center for education, conservation, and community engagement. Recognized as a Garden of National Significance and protected as a Heritage Area, the garden hosts educational programs, guided tours, events like Gardens Magic, and is accessible via the iconic Cable Car.",
        "Category": "Plant",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab12",
        "Country": "New Zealand",
        "City": "Dargaville",
        "GeoLocation": "-35.60111, 173.52722",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/god_of_the_forest.jpg",
        "Description": "Tāne Mahuta-\"God of the Forest\"",
        "DetailedDescription": "Tāne Mahuta is the largest living kauri tree known today, estimated to be between 1,250 and 2,500 years old and towering at about 45.2 m (148 ft) with a girth exceeding 15 m. Named after the Māori god Tāne, the tree stands as a revered symbol of natural heritage and is a remnant of the ancient subtropical rainforest of the Northland Peninsula. It was first spotted by road surveyors in the 1920s when preparing State Highway 12, and has since become an iconic conservation focus, with efforts to protect it from kauri dieback disease including trail management and hygiene stations. The short, wheelchair-accessible walk to see this majestic tree draws around 200,000 visitors annually.",
        "Category": "Plant",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab13",
        "Country": "New Zealand",
        "City": "Whangaroa Harbour",
        "GeoLocation": "-34.9833, 173.6167",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/rikoriko_cave.jpg",
        "Description": "Rikoriko Sea Cave",
        "DetailedDescription": "Rikoriko Sea Cave, located in Whangaroa Harbour, is renowned as the world's largest sea cave by volume. Accessible only by boat, this cave boasts a dramatic entrance and a vast interior that can accommodate large vessels. The cave is a popular spot for tourists seeking unique marine experiences, including guided boat tours that showcase its impressive size and natural beauty. Its remote location and grandeur make it a hidden gem for adventurers exploring New Zealand's rugged coastline.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab14",
        "Country": "New Zealand",
        "City": "Kahurangi National Park",
        "GeoLocation": "–41.223, 172.039",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/oparara_basin.jpg",
        "Description": "Ōpārara Basin",
        "DetailedDescription": "Ōpārara Basin is a remote and unspoiled temperate rainforest featuring dramatic natural rock arches, a labyrinth of caves, and rich fossil beds. The area is celebrated for its spectacular limestone arches like the Ōpārara Arch and Moria Gate, formed in an ancient honeycomb karst system. It also contains significant paleontological sites, including the largest collection of bird fossils found in New Zealand, and even rare moss species unique to the basin. Visitor access is facilitated through well-maintained walkways and trails—such as Mirror Tarn and Box Canyon—along with guided tours for the Honeycomb Hill Caves.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab15",
        "Country": "New Zealand",
        "City": "Fiordland National Park",
        "GeoLocation": "–44.648281, 167.905777",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/milford_sound.jpg",
        "Description": "Milford Sound",
        "DetailedDescription": "Milford Sound is a dramatic glacially-carved fiord within Fiordland National Park, stretching about 15 km inland with sheer cliffs rising over 1,200 m above dark, inky waters. The fiord features permanent waterfalls such as Lady Bowen Falls (162 m) and Stirling Falls, while dozens of temporary cascades spring to life after rainfall. It is home to diverse wildlife including bottlenose dolphins, seals, penguins, and even black coral closer to the surface due to tannin-laden freshwater layers. Accessible by road via the Homer Tunnel, Milford Sound is often called the \"eighth wonder of the world\" and remains one of New Zealand's most iconic natural attractions.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab16",
        "Country": "New Zealand",
        "City": "Maerewhenua Valley",
        "GeoLocation": "–44.8935, 170.6562",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/elephant_rocks.jpg",
        "Description": "Elephant Rocks",
        "DetailedDescription": "Elephant Rocks is a collection of large, weathered limestone boulders scattered across a gentle hillside on a private farm near Duntroon. The formations are remnants of the Otekaike Limestone formation and are famed for their rounded, sculptural appearance, evocative of elephant shapes. The site is accessible via a short, informal walk across farmland, and is a recognized filming location for The Chronicles of Narnia (Aslan's camp). The rugged geology of the site, combined with its pastoral setting and film connection, make it a quirky and memorable stop off the beaten path.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab17",
        "Country": "New Zealand",
        "City": "Taupō",
        "GeoLocation": "–38.658, 176.091",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/craters_of_the_moon.jpg",
        "Description": "Craters of the Moon",
        "DetailedDescription": "Craters of the Moon is a geothermal area characterized by numerous steam vents and hydrothermal eruption craters that constantly shift, collapse, and reform, giving the whole area an unearthly, desolate appearance. Visitors can explore the site via boardwalks on a main track circuit that typically takes around 45 minutes, with an optional steeper loop to a viewing point. Only a few hardy plant species like prostrate kānuka, ferns, and mosses survive in the heated soils. The area's strange landscape and sulphur scent evoke a lunar-like atmosphere—and it's managed by the Department of Conservation with support from the Craters of the Moon Trust.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab18",
        "Country": "New Zealand",
        "City": "Wellington",
        "GeoLocation": "−40.900446, 176.231462",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/castle_point_lighthouse.jpg",
        "Description": "Castle Point Lighthouse",
        "DetailedDescription": "Castle Point Lighthouse is a majestic cast-iron lighthouse first lit in 1913.  Lighthouse Index. The tower is 23 m tall, but due to its cliff location its focal height is 52 m above sea level, allowing its light to be seen up to about 26 nautical miles out to sea. It was one of the last manually operated lighthouses; it was automated in 1988.  The walk to the lighthouse from Castlepoint township via Lighthouse Walk is about 30 minutes return, offering dramatic coastal views and opportunities to see fur seals and fossil shells.",
        "Category": "Place",
        "KnowledgeType": "Historical"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab19",
        "Country": "New Zealand",
        "City": "Otago Region",
        "GeoLocation": "−45.351555, 170.825468",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/moeraki_boulders.jpeg",
        "Description": "Moeraki Boulders",
        "DetailedDescription": "The Moeraki Boulders are unusually large spherical grey septarian concretions lying along a stretch of Koekohe Beach; they formed millions of years ago in ancient seabed mudstone and have been exposed and concentrated on the beach by coastal erosion; some boulders are as large as three metres in diameter, and local Māori legends claim they are the remains of eel baskets and food baskets from the wreck of the canoe Āraiteuru; the site is protected as a scientific reserve and is a popular and photogenic stop along the East Otago coast.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab20",
        "Country": "New Zealand",
        "City": "Waikato Region",
        "GeoLocation": "−36.89025, 175.82213",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/hot_water_beach.jpg",
        "Description": "Hot Water Beach",
        "DetailedDescription": "Hot Water Beach is a beach famous for underground hot springs that filter up through sand between high and low tide; visitors dig their own hot pools in the sand during low tide and soak in water as hot as 64°C; the springs are located close to offshore rocks and accessible only within about two hours either side of low tide; the beach attracts many tourists who bring spades and buckets and is a popular geothermal attraction in the Waikato region.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab21",
        "Country": "New Zealand",
        "City": "Canterbury Region",
        "GeoLocation": "−43.6045, 170.1425",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/hooker_valley_track.jpg",
        "Description": "Hooker Valley Track",
        "DetailedDescription": "The Hooker Valley Track is a popular 10 km round-trip hike beginning at White Horse Hill, with views of alpine tussock, glaciers, hanging valleys, suspension bridges, and ending at Hooker Lake which often has icebergs floating in it; the trail is well-formed with minimal elevation gain making it accessible to many visitors; at the end there is a lookout offering unobstructed views of Aoraki / Mount Cook across the lake; in summer the flora includes Mount Cook lily, daisies, and high alpine grasses.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab22",
        "Country": "New Zealand",
        "City": "Wellington",
        "GeoLocation": "−41.29444, 174.75000",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/zealandia.jpg",
        "Description": "Zealandia",
        "DetailedDescription": "Zealandia is a fenced urban ecosanctuary of about 225 ha focused on restoring native forest and wildlife; it is home to more than 30 native bird species including rare takahe and little spotted kiwi, as well as tuatara; it has over 30 km of walking tracks, free shuttles from central Wellington, and guided night tours to see nocturnal species; the sanctuary demonstrates conservation techniques, predator control, and community engagement in restoring biodiversity in an urban context.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab23",
        "Country": "New Zealand",
        "City": "Taranaki Region",
        "GeoLocation": "−39.296667, 174.070556",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/mount_taranaki.jpg",
        "Description": "Mount Taranaki",
        "DetailedDescription": "Taranaki Maunga is a near-perfect symmetrical stratovolcano rising to 2,518 meters with a secondary cone called Fanthams Peak; it is sacred in Māori tradition, known for its stories such as the battle with Tongariro and its journey west across rivers; its slopes include dense rainforest, subalpine herbfields and alpine zones, and it lies within Te Papa-Kura-o-Taranaki (Egmont National Park), which has multiple walking tracks including the Around the Mountain Circuit and the Pouākai Circuit; recently the mountain and its surrounding peaks were granted legal personhood in recognition of their cultural and spiritual significance.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab24",
        "Country": "New Zealand",
        "City": "Canterbury Region",
        "GeoLocation": "−43.2308, 171.7161",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/castle_hill.jpg",
        "Description": "Castle Hill",
        "DetailedDescription": "Castle Hill (Kura Tāwhiti) is a limestone boulder field and conservation area featuring sculpted rock formations scattered across high country landscapes; it is famous for bouldering, hiking, and dramatic scenery including large outcrops of limestone that resemble a ruined castle; accessible via a short walk from a car park off SH 73, visitors can explore trails among the rocks and enjoy views of the Craigieburn and Torlesse Ranges; the site holds cultural significance to Māori, especially Ngāi Tahu, who used rock shelters here and named the place \"Kura Tāwhiti\" meaning \"treasure from a distant land.\"",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab25",
        "Country": "New Zealand",
        "City": "Rotorua",
        "GeoLocation": "−38.16013, 176.25111",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/pohutu_geyser.jpg",
        "Description": "Pōhutu Geyser",
        "DetailedDescription": "Pōhutu Geyser is the largest geyser in the Southern Hemisphere and one of Rotorua's most active geothermal features, erupting up to twenty times a day, sometimes reaching heights of around 30 metres; it sits in a valley filled with many hot springs, pools and steam vents and is deeply significant in Māori tradition for its name and its role in local geothermal culture; visitors can view eruptions from safe platforms and walk among other geothermal features in Whakarewarewa.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab26",
        "Country": "New Zealand",
        "City": "Wellington",
        "GeoLocation": "−41.306423, 174.824291",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/weta_workshop.jpg",
        "Description": "Wētā Workshop",
        "DetailedDescription": "Wētā Workshop is a world-renowned motion picture effects and prop company founded in 1987; its Wētā Cave and workshop tours in Miramar allow visitors to see behind the scenes how costumes, weapons, creatures and miniatures are made for major films such as The Lord of the Rings, The Hobbit, Avatar and more; the site includes a retail \"cave\" of movie memorabilia, guided tours through creative departments, and interactive exhibits; it is a major draw for film buffs and those interested in special effects craftsmanship.",
        "Category": "Art",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab27",
        "Country": "New Zealand",
        "City": "Tasman District",
        "GeoLocation": "−40.9943, 172.8790",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/wharariki_beach.jpg",
        "Description": "Wharariki Beach",
        "DetailedDescription": "Wharariki Beach is a wild, windswept stretch of coastline framed by towering rock arches called the Archway Islands, rolling dunes, caves, and dramatic cliffs overlooking the Tasman Sea; accessible via a 20-minute walk from the end of Wharariki Road through farmland and coastal forest, the beach is notable for its seal colony, tide pools, and spectacular sunsets at low tide; it is remote, largely undeveloped, and one of New Zealand's most photographed beaches.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab28",
        "Country": "Canada",
        "City": "Alberta",
        "GeoLocation": "51.4968, 115.9281",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/banff_national_park.jpg",
        "Description": "Banff National Park",
        "DetailedDescription": "Banff National Park, established in 1885, is Canada's oldest national park and a UNESCO World Heritage Site. Located in the Canadian Rockies, it spans over 6,600 square kilometers and is renowned for its stunning mountain landscapes, crystal-clear lakes like Lake Louise and Moraine Lake, and diverse wildlife including grizzly bears, elk, and bighorn sheep. Visitors can enjoy activities such as hiking, skiing, and hot springs, making it a year-round destination for nature enthusiasts.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab29",
        "Country": "United States",
        "City": "Arizona",
        "GeoLocation": "36.8619, 111.3743",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/antelope_canyon.jpg",
        "Description": "Antelope Canyon",
        "DetailedDescription": "Antelope Canyon is a slot canyon in the American Southwest, renowned for its wave-like structure and the play of light and shadow that creates a surreal visual experience. The canyon is divided into two sections: Upper Antelope Canyon, known for its light beams and accessibility, and Lower Antelope Canyon, which offers a more adventurous experience with narrow passageways. Formed over thousands of years by flash flooding and erosion, it is a popular destination for photographers and nature enthusiasts.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab30",
        "Country": "United Kingdom",
        "City": "Northern Ireland",
        "GeoLocation": "55.2400, 6.5110",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/causeway_coast.jpg",
        "Description": "Causeway Coast",
        "DetailedDescription": "The Giant's Causeway and Causeway Coast is a UNESCO World Heritage Site renowned for its unique geological formations. It features around 40,000 interlocking basalt columns resulting from ancient volcanic activity. The site is steeped in myth, with local legends attributing its creation to the Irish giant Finn MacCool. Visitors can explore the dramatic coastline, enjoy panoramic views, and experience the rich history and folklore associated with this natural wonder.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab31",
        "Country": "Turkey",
        "City": "Denizli Province",
        "GeoLocation": "37.9239, 29.1233",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/pamukkale.jpg",
        "Description": "Pamukkale",
        "DetailedDescription": "Pamukkale, meaning \"Cotton Castle\" in Turkish, is a natural site in southwestern Turkey, famous for its white travertine terraces formed by calcite-laden thermal waters. The terraces are part of the Hierapolis-Pamukkale UNESCO World Heritage Site, which includes the ancient Greek city of Hierapolis. The site has been a destination for thermal spring bathing since antiquity and continues to attract visitors for its unique geological formations and historical significance.",
        "Category": "Place",
        "KnowledgeType": "Modern"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab32",
        "Country": "China",
        "City": "Xiamen",
        "GeoLocation": "24.4444, 118.0789",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/gulangyu_island.jpg",
        "Description": "Gulangyu Island",
        "DetailedDescription": "Gulangyu Island, located just off the coast of Xiamen, is renowned for its serene environment, colonial architecture, and rich cultural heritage. The island is car-free, offering visitors a peaceful retreat with winding lanes, lush greenery, and historical buildings. It is also known for its piano museum, showcasing the island's musical legacy. Gulangyu has been recognized as a UNESCO World Heritage Site for its unique blend of cultural and natural attractions.",
        "Category": "Place",
        "KnowledgeType": "Traditonal"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab33",
        "Country": "India",
        "City": "Agra",
        "GeoLocation": "27.1751, 78.0421",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/taj_mahal.jpg",
        "Description": "Taj Mahal",
        "DetailedDescription": "The Taj Mahal is a white marble mausoleum located on the southern bank of the Yamuna River in Agra, India. Commissioned in 1632 by Mughal emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal, it is widely regarded as one of the most beautiful buildings ever created. The Taj Mahal is renowned for its symmetrical design, intricate inlay work, and the use of white marble that reflects hues according to the intensity of sunlight or moonlight. It was designated as a UNESCO World Heritage Site in 1983 and attracts millions of visitors annually.",
        "Category": "Place",
        "KnowledgeType": "Historical"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab34",
        "Country": "Peru",
        "City": "Cusco Region",
        "GeoLocation": "13.1631, -72.5450",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/machu_picchu.jpg",
        "Description": "Machu Picchu",
        "DetailedDescription": "Machu Picchu is a 15th-century Inca citadel located in the Andes Mountains of Peru. Built under the reign of Inca emperor Pachacuti, it is renowned for its dry-stone construction and panoramic views. The site includes temples, terraces, and agricultural areas, reflecting the advanced engineering and cultural practices of the Inca civilization. Rediscovered in 1911 by American historian Hiram Bingham, Machu Picchu has since become a UNESCO World Heritage Site and one of the New Seven Wonders of the World. Despite facing challenges such as overtourism and natural threats, efforts continue to preserve its historical and cultural significance.",
        "Category": "Place",
        "KnowledgeType": "Historical"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab35",
        "Country": "Egypt",
        "City": "Giza Governorate",
        "GeoLocation": "29.9792, 31.1342",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/giza_pyramid.jpg",
        "Description": "Great Pyramid of Giza",
        "DetailedDescription": "The Great Pyramid of Giza, also known as the Pyramid of Khufu or Cheops, is the largest of the three pyramids on the Giza Plateau. Constructed during the Fourth Dynasty of the Old Kingdom around 2580–2560 BCE, it served as the tomb for Pharaoh Khufu. Originally standing at 146.6 meters, it was the tallest man-made structure for over 3,800 years. The pyramid is renowned for its precise alignment and massive scale, with an estimated 2.3 million stone blocks, each weighing an average of 2.5 to 15 tons. It remains the only surviving wonder of the Seven Wonders of the Ancient World and is part of the Memphis and its Necropolis – the Pyramid Fields from Giza to Dahshur UNESCO World Heritage Site.",
        "Category": "Place",
        "KnowledgeType": "Historical"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab36",
        "Country": "Cambodia",
        "City": "Siem Reap",
        "GeoLocation": "13.4125, 103.8667",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/angkor_wat.jpg",
        "Description": "Angkor Wat",
        "DetailedDescription": "Angkor Wat is a vast temple complex in northern Cambodia, originally constructed in the early 12th century by King Suryavarman II as a Hindu temple dedicated to the god Vishnu. It is renowned for its grandeur and architectural sophistication, covering an area of over 400 acres. The temple is designed to represent Mount Meru, the center of the universe in Hindu and Buddhist cosmology. Angkor Wat is one of the most important archaeological sites in Southeast Asia and is a UNESCO World Heritage Site. It is also the largest religious monument in the world.",
        "Category": "Place",
        "KnowledgeType": "Historical"
    },
    {
        "UserID": "kciN",
        "RecordID": "434ee49c-0375-45fa-b8bb-a54914006ab37",
        "Country": "Japan",
        "City": "Kyoto",
        "GeoLocation": "35.0116, 135.7850",
        "S3ImageURL": "https://d2ln0jlxttrevg.cloudfront.net/uploads/kiyomizu-dera.jpg",
        "Description": "Kiyomizu-dera",
        "DetailedDescription": "Kiyomizu-dera, officially known as Otawa-san Kiyomizu-dera, is a historic Buddhist temple in eastern Kyoto. Founded in 778, it is renowned for its vast wooden stage that juts out over the hillside, supported by hundreds of wooden pillars. The temple is dedicated to Kannon, the Goddess of Mercy, and is part of the Historic Monuments of Ancient Kyoto UNESCO World Heritage Site. Visitors often come to pray for good health and love, and the temple's name, \"Kiyomizu,\" translates to \"pure water,\" derived from the Otawa Waterfall running through the temple grounds.",
        "Category": "Place",
        "KnowledgeType": "Historical"
    }
]
    # #3 - Insert Data
    for each in input:
        table.put_item(Item=each)
    # table.put_item(Item=input)
    # print('Successfully put item')

    #4 - Scan Table
    scanResponse = table.scan(TableName=TABLE_NAME)
    items = scanResponse['Items']
    for item in items:
        print(item)


main()