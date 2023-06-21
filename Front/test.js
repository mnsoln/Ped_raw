import { isEqual } from 'lodash-es'


const PEDS=[
    {
    "id":"Jean Pierre",
    "alias":"JP",
    "pere":"LM",
    "mere":"JM",
    "sexe":"M",
    "phenotype":"Atteint",
    "listeHPO":"LDL",
    "tagStark":"41",
    }
]

const pedd= [
    {
    "id":"Jean Pierre",
    "alias":"JP",
    "pere":"LM",
    "mere":"JM",
    "sexe":"M",
    "phenotype":"Atteint",
    "listeHPO":"LDL",
    "tagStark":"41",
    }
]

console.log('lol')
console.log(isEqual(pedd, PEDS))