# Entity Map
```
<entity>
    <generalInfo>
    <sanctionsLists>
    <sanctionsPrograms>
    <sanctionsTypes>
    <legalAuthorities>
    <names>
    <addresses>
    <features>
    <identityDocuments>
    <relationships>
```

## General Information
```
<generalInfo>
    <identityId>
    <entityType>
    <title>            # Some
    <remarks>          # Some
```

## Listing Information
```
<sanctionsLists>
    <sanctionsList> ...
<sanctionsPrograms>
    <sanctionsProgram> ...
<sanctionsTypes>
    <sanctionsType>
<legalAuthorities>
    <legalAuthority> ...
```

## Name 
```
<name> ...
    <isPrimary>
    <aliasType>
    <isLowQuality>
    <translations>
        <translation> ...
            <isPrimary>
            <script>
            <formattedFirstName>
            <formattedLastName>
            <formattedFullName>
            <nameParts>
                <namePart> ...
                    <type>
                    <value>
```

## Addresses
```
<address> ...
    <country>
    <translations>
        <translation>
            <isPrimary>
            <script>
```

## Feature

```
<feature> ...
    type
    versionId
    value
    valueDate
        fromDateBegin
        fromDateEnd
        toDateBegin
        toDateEnd
        isApproximate
        isDateRange
    valueRefId
    isPrimary
```

## Identity Documents
```
<identityDocument> ...
    <type>
    <name>
    <documentNumber>
    <isValid>
    <issuingCountry>
```

## Relationships
```
<relationship> ...
    <type>
    <relatedEntity>
```