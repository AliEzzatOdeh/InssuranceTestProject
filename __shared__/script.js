var link = 'http://127.0.0.1:8000/api/getAllRiskTypes';
var risks;
var parentForm = document.getElementById("fieldsForm");

var riskList = new Vue({
    delimiters: ['[[', ']]'],
    el: '#riskList',

    data: {
        risks: []
    },

    methods: {
        indexChats: function() {
            var me =this;

            this.$http.get(link).then((response) => {
               
                
                this.$set(this.risks, response.bodyText);
                const resultArray = [];
                var data = response.body;

                for(let key in data){
                    resultArray.push(data[key]);
                  }
                  me.risks = resultArray;
            }, (response) => {
                console.log('could not fetch risks from api');
            });
        }
    },

    mounted: function() {
        this.indexChats();
    }
});

function FieldInfo(field){
    this.name = field.name;
    this.type= field.field_type;

    this.getValue = function(){
        var returnedValue = "";

        switch(this.type)
        {
        case "text":
        returnedValue =field.value;
        break;
        case "number":
        returnedValue = parseInt(field.value);
        break;
        case "date":
        returnedValue = formatDate(field.value);
        break;
        case "enum": 
        returnedValue = [];
        field.enum_values.forEach( (element) => returnedValue.push(element.enum_value));
        break;
        }

        return returnedValue;
    }

    function formatDate(input){
        var formattedDate = "";
        var years = input.substring(0, 4);
        var months = input.substring(4, 6);
        var days = input.substring(6);

        formattedDate = years + "-" + months + "-" + days;

        return formattedDate;
    }
}

function handleRiskClick(riskElement){

    clearForm();
    if(riskElement.fields.length > 1) {
        riskElement.fields.forEach(function(field){
        createFieldElement(field);
    });
    } 
    else {
    addNoFieldsElementToForm(riskElement.name);
    }                   
}

function createFieldElement(field){
    var inputNode;
    var choices;
    
    var containerFieldElement = document.createElement('div');
    containerFieldElement.className = "field-container";
    
    var labelNode = document.createElement('label');
    labelNode.innerHTML = field.name;

    var fieldInfo = new FieldInfo(field);
  
    if(fieldInfo.type != "enum"){
        inputNode = document.createElement('input');
        inputNode.type = fieldInfo.type;
        inputNode.value = fieldInfo.getValue();
    }  else {
        inputNode = document.createElement('select');

        choices =  fieldInfo.getValue();

        choices.forEach((element) => {
            var optionNode = document.createElement('option');
            optionNode.innerHTML = element;
            optionNode.value = element;
            inputNode.appendChild(optionNode);
        });
    }
    
    containerFieldElement.appendChild(labelNode);
    containerFieldElement.appendChild(inputNode);
    parentForm.appendChild(containerFieldElement);
}

function clearForm(){
    while (parentForm.firstChild) {
        parentForm.removeChild(parentForm.firstChild);
    }
}

function addNoFieldsElementToForm(riskName){
    var emptyFieldsNode = document.createElement('label');
    emptyFieldsNode.innerHTML = "No fields added for " + riskName;
    parentForm.appendChild(emptyFieldsNode);
}