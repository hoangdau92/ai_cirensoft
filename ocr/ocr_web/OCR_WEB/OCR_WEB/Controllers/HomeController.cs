using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;

namespace OCR_WEB.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<ActionResult> Index(FormCollection fc, HttpPostedFileBase file)
        {
            try
            {
                if (file != null && file.ContentLength > 0)
                    try
                    {
                        byte[] fileInBytes = new byte[file.ContentLength];
                        using (BinaryReader theReader = new BinaryReader(file.InputStream))
                        {
                            fileInBytes = theReader.ReadBytes(file.ContentLength);
                        }
                        string fileAsString = Convert.ToBase64String(fileInBytes);

                        using (var client = new HttpClient())
                        {
                            client.BaseAddress = new Uri("http://10.151.137.202:6790");
                            var content = new FormUrlEncodedContent(new[]
                            {
                                new KeyValuePair<string, string>("image", fileAsString)
                            });
                            var result = await client.PostAsync("/predict", content);
                            string resultContent = await result.Content.ReadAsStringAsync();
                            var emp = JsonConvert.DeserializeObject<OCR_Result>(resultContent);

                            ViewBag.RESULT = emp.text;
                            //var base64 = Convert.ToBase64String(Model.ByteArray);
                            var imgSrc = String.Format("data:image/gif;base64,{0}", fileAsString);
                            ViewBag.IMG = imgSrc;

                        }

                        ViewBag.Message = "Convert successfully";
                    }
                    catch (Exception ex)
                    {
                        ViewBag.Message = "ERROR:" + ex.Message.ToString();
                    }
                else
                {
                    ViewBag.Message = "You have not specified a file.";
                }
                return View();
            }
            catch (Exception ex)
            {
                return View();
            }
        }

        public static string Base64Decode(string base64EncodedData)
        {
            var base64EncodedBytes = Convert.FromBase64String(base64EncodedData);
            return System.Text.Encoding.UTF8.GetString(base64EncodedBytes);
        }

        public class OCR_Result
        {
            public bool success { get; set; }
            public string text { get; set; }
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}