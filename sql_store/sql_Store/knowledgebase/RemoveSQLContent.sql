CREATE PROC [knowledgebase].[RemoveSQLContent](
    @container varchar(500),
    @directory varchar(1000),
    @filePath varchar(1000)
)
AS
BEGIN
    -- Emdedding has a foreign key from Content and Content & Redactlog has a foreign key from Document
    -- We start deleting from Embedding then Content, then Redact Logs and then update the document status as Completed

    BEGIN TRANSACTION;
    BEGIN TRY

        DELETE e 
        FROM knowledgebase.Embeddings e 
        JOIN knowledgebase.Content c ON e.ContentId = c.ID
        JOIN knowledgebase.Document d ON c.DocumentId = d.ID
        where d.Destination = @container+'/'+@directory+'/'+@filePath    

        DELETE C
        FROM knowledgebase.Content c
        JOIN knowledgebase.Document d ON c.DocumentId = d.ID
        where d.Destination = @container+'/'+@directory+'/'+@filePath        

    COMMIT;
    END TRY
    BEGIN CATCH
        -- If there is any error, rollback the transaction
        ROLLBACK;
        -- Re-throw the error
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR (@ErrorMessage, -- Message text.
                   16, -- Severity.
                   1 -- State.
                   );
    END CATCH;
END;

GO

