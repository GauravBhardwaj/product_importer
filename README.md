export DATABASE_URL="postgresql://localhost/product_dev"



#should i hhave ??
# using dask, pandas to read csv
# should have chunked data upload from UI
# shhould have used multiple session.merge() to update duplicates ?
# inserting one by one vs many in one go?
# putting uniques together by reading csv and putting it in cache. in O(n)
# UI creation - will take time



STEPS:-

- GO to https://fulfill-product-importer.herokuapp.com/login
- username 'gb' password 'gb'
- directs you to upload page
- upload your ccsv file, as it progresses file gets queued for processing
- you should see streaming products on the same page if redis pub-sub works
- VISIT https://fulfill-product-importer.herokuapp.com/products
    - list all products
    - add new prpducts
    - update existing product
    - filter/ search product
- https://fulfill-product-importer.herokuapp.com/drop-products with DELETE method is for dropping all products

TODO-

- exceptional handling
- handle bad inputs in file
- handle connection retrials
- Enhance UI
- Tasks are saved for each job, we can implement a dashboard for live progress as well.
-