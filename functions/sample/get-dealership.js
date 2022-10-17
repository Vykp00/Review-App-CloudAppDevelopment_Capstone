
// RETURN ALL DEALERSHIPS: the problem is it still see the title "docs":{ doc:}
    const { CloudantV1 } = require('@ibm-cloud/cloudant');
    const { IamAuthenticator } = require('ibm-cloud-sdk-core');
    
    async function main(params) {
        screat={
            "COUCH_URL": "https://19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix.cloudantnosqldb.appdomain.cloud",
            "IAM_API_KEY": "4-PnQyyuvd8ON4UvdiTLGv84UftA0HTQddgoGHASWaxA",
            "COUCH_USERNAME": "19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix",
        };
        const authenticator = new IamAuthenticator({ apikey: screat.IAM_API_KEY })
        const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
        });
        cloudant.setServiceUrl(screat.COUCH_URL);
            try {
                let dbDoc = await cloudant.postAllDocs({
                    db: 'dealerships',
                    includeDocs: true,
                });
                return { "docs": dbDoc.result.rows};
                } catch (error) {
                    return { error: error.description };
                }
      }

// Debugg this version later
      const { CloudantV1 } = require('@ibm-cloud/cloudant');

      async function main(params) { 
      
        secret={
            "COUCH_URL": "https://19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix.cloudantnosqldb.appdomain.cloud",
            "IAM_API_KEY": "4-PnQyyuvd8ON4UvdiTLGv84UftA0HTQddgoGHASWaxA",
            "COUCH_USERNAME": "19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix",
        };
      
      const cloudant = CloudantV1({ 
      
              url: secret.COUCH_URL, 
      
              plugins: { iamauth: { iamApiKey: secret.IAM_API_KEY } } 
      
          }); 
      
          let dbListPromise = await getDbs(cloudant); 
      
          return dbListPromise; 
      
      } 
      
       
      
      function getDbs(cloudant) { 
      
          return new Promise((resolve, reject) => { 
      
              let db = cloudant.use('dealerships'); 
      
              let result = db.list( {fields : ['id','city','state','st','address','zip','lat','long','short_name','full_name'], include_docs:true} ) 
      
                  .then(result => { 
      
                      resolve({ dealerships: result }) 
      
                  }) 
      
                  .catch(err => { 
      
                      reject({ err: err}); 
      
                  }); 
      
          }); 
      
      } 