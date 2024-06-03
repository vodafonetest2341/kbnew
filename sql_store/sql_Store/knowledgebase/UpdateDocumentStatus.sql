CREATE PROC [knowledgebase].[UpdateDocumentStatus](
    @container varchar(1000),
    @directory varchar(1000),
    @filePath varchar(1000),
    @Status varchar(500)
    )
AS
    Update knowledgebase.Document
     SET Status = @Status, UpdatedAt = getdate()
    where 
    Destination = @container+'/'+@directory+'/'+@filePath

GO

