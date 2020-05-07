//Edit 'key' and 'columns' to connect your spreadsheet

//enter google sheets key here




//"data" refers to the column name with no spaces and no capitals
//punctuation or numbers in your column name
//"title" is the column name you want to appear in the published table


$(document).ready(function() {
   $('select').change(function() {
   //alert(this.value);
   if(this.value=="l2")
   {
   var key =
  "1Tkz63YcCbRZz0rp-kKYJAv3PW2AteWmA1ByNrf3Txnk";
  var columns = [{
  "data": "district",
  "title": "State Initiatives/District"
}, {
  "data": "category",
  "title": "Category"
}, {
  "data": "initiatives",
  "title": "Initiatives"
},{
  "data": "helpline",
  "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
            $(nTd).html("<a href='tel:"+oData.helpline+"'>"+oData.helpline+"</a>");},
  "title": "Helpline nos"
},{
  "data": "link",
  "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
            $(nTd).html("<a href='"+oData.link+"'>"+oData.link+"</a>");},
  "title": "Link"
},{
  "data": "eligibility",
  "title": "Eligibility"
},{
  "data": "document",
  "title": "Document"
},{
  "data": "duration",
  "title": "Duration"
},{
  "data": "info",
  "title": "Others"
}];}
  else if(this.value=="l1")
  {
    var key="1gBZJ5o_UHRpTmt7tdxg2wJF5ZgSsKG_HzInMckZlJLI";
    var columns = [{
  "data": "state",
  "title": "State Services/District Control"
}, {
  "data": "helpline",
  "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
            $(nTd).html("<a href='tel:"+oData.helpline+"'>"+oData.helpline+"</a>");},
  "title": "Helpline nos"
}, {
  "data": "email",
  "title": "Email Address"
},{
  "data": "link",
  "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
            $(nTd).html("<a href='"+oData.link+"'>"+oData.link+"</a>");},
  "title": "Link"
}];
  }

  function initializeTabletopObject() {
    Tabletop.init({
      key: key,
      callback: function(data, tabletop) {
        writeTable(data); //call up datatables function
      },
      simpleSheet: true,
      debug: false
    });
  }

  initializeTabletopObject();

  function writeTable(data) {
    //select main div and put a table there
    //use bootstrap css to customize table style: http://getbootstrap.com/css/#tables
    $('#graphic').html(
      '<table cellpadding="0" cellspacing="10px" border="10px" class="table table-striped table-condensed table-responsive" id="mySelection"></table>'
    );

    //initialize the DataTable object and put settings in
    $("#mySelection").DataTable({
      "autoWidth": false,
      "data": data,
      "columns": columns,
      "ordering": false,
      "pagingType": "simple" //no page numbers
        //uncomment these options to simplify your table
        //"paging": false,
        //"searching": false,
        //"info": false
    });
  }});
});
//end of writeTable