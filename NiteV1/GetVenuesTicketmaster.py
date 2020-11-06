import ticketpy

tm_client = ticketpy.ApiClient('LWq6J1B993ouxA9Aj0YXvsgP5U9eCHdV')
# pages = tm_client.events.find(
#     classification_name='bar',
#     country_code='GB',
#     start_date_time='2017-05-19T20:00:00Z',
#     latlong='51.488710,-0.142030',
#     radius=25
# )
# for page in pages:
#     for event in page:
#         print(event)

venues = tm_client.venues.find(country_code='GB', latlong='51.488710,-0.142030', radius=1, units='km', classification_name='bar').all()
for v in venues:
    print('Name: ', v.name)
    print('Address: ', v.postal_code)
    print('URL: ', v.url)
    print(v.box_office_info)
    print(v.dmas)
    print(v.markets)
    print(v.general_info)
    print(v.links)

# classifications = tm_client.classifications.find(keyword="bar").one()

# for cl in classifications:
#     print("Segment: {}".format(cl.segment.name))
#     for genre in cl.segment.genres:
#         print("--Genre: {}".format(genre.name))