// GET BY STATE
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
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
    const selector= CloudantV1.JsonObject = {
        state: {
            "$eq": params.state
        }
      };
    let dbListPromise = getMatchingRecords(cloudant, selector);
    return dbListPromise;
}
function getMatchingRecords(cloudant, selector) {
    return new Promise((resolve, reject) => {
        cloudant.postFind({
            db: 'dealerships',
            selector: selector,
        }).then((result)=>{
            resolve({result:result.result.docs});
        })
        .catch(err => {
            console.log(err);
            reject({ err: err });
        });
         })
}
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
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
function main(params) { 
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
    return { 
  
      entries: params.dealerships.rows.map((row) => { return { 
  
        id: row.doc.id, 
  
        city: row.doc.city, 
  
        state:row.doc.state, 
  
        st:row.doc.st, 
  
        address:row.doc.address, 
  
        zip:row.doc.zip, 
  
        lat:row.doc.lat, 
  
        long:row.doc.long 
  
      }}) 
  
    }; 
  
  }  